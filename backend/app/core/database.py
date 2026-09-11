import os
import uuid
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

import urllib.parse

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL or "[YOUR" in DATABASE_URL or "YOUR-PASSWORD" in DATABASE_URL or "YOUR_PASSWORD" in DATABASE_URL:
    DATABASE_URL = "sqlite:////tmp/careeros.db"
else:
    try:
        if "://" in DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
            scheme, rest = DATABASE_URL.split("://", 1)
            if "@" in rest:
                auth_part, host_part = rest.rsplit("@", 1)
                if ":" in auth_part:
                    user, password = auth_part.split(":", 1)
                    encoded_password = urllib.parse.quote(urllib.parse.unquote(password), safe="")
                    rest = f"{user}:{encoded_password}@{host_part}"
            DATABASE_URL = f"{scheme}://{rest}"
    except Exception:
        pass

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+pg8000://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+pg8000" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)

if DATABASE_URL.startswith("sqlite:///./"):
    db_file = DATABASE_URL.replace("sqlite:///./", "")
    abs_db_path = (Path(__file__).resolve().parents[2] / db_file).as_posix()
    DATABASE_URL = f"sqlite:///{abs_db_path}"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=300
    )
except Exception:
    engine = create_engine(
        "sqlite:////tmp/careeros.db",
        connect_args={"check_same_thread": False}
    )


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL/CockroachDB UUID type, otherwise uses CHAR(36), handling string and UUID object conversions seamlessly.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name in ('postgresql', 'cockroachdb'):
            try:
                from sqlalchemy.dialects.postgresql import UUID as PG_UUID
                return dialect.type_descriptor(PG_UUID(as_uuid=True))
            except ImportError:
                return dialect.type_descriptor(CHAR(36))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name in ('postgresql', 'cockroachdb'):
            if isinstance(value, uuid.UUID):
                return value
            try:
                return uuid.UUID(str(value))
            except (ValueError, TypeError):
                return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            try:
                return str(uuid.UUID(str(value)))
            except (ValueError, TypeError):
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        try:
            return uuid.UUID(str(value))
        except (ValueError, TypeError):
            return value


def get_db():
    try:
        db = SessionLocal()
        # Ping connection to verify credentials
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
    except Exception as e:
        logging.getLogger("careeros.db").error(f"Database connection failure ({e}). Falling back to local SQLite.")
        sqlite_engine = create_engine("sqlite:////tmp/careeros.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=sqlite_engine)
        FallbackSession = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
        db = FallbackSession()

    try:
        yield db
    finally:
        try:
            db.close()
        except Exception:
            pass