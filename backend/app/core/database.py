import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL or "[YOUR" in DATABASE_URL or "YOUR-PASSWORD" in DATABASE_URL or "YOUR_PASSWORD" in DATABASE_URL:
    DATABASE_URL = "sqlite:////tmp/careeros.db"

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
        yield db
    except Exception as e:
        logging.getLogger("careeros.db").error(f"Database connection failure ({e}). Falling back to local SQLite.")
        sqlite_engine = create_engine("sqlite:////tmp/careeros.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=sqlite_engine)
        FallbackSession = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
        db = FallbackSession()
        yield db
    finally:
        try:
            db.close()
        except Exception:
            pass