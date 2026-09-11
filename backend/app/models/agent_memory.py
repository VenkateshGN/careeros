import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text, ForeignKey, JSON, TypeDecorator

from app.core.database import Base, GUID

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = None

class CrossVector(TypeDecorator):
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name in ('postgresql', 'cockroachdb') and Vector is not None:
            return dialect.type_descriptor(Vector(1536))
        return dialect.type_descriptor(JSON)

class AgentMemory(Base):
    """
    Dedicated schema fulfilling the 'Agentic Memory' system of record architecture for CockroachDB/PostgreSQL/MySQL.
    """
    __tablename__ = "agent_memories"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(200), nullable=True, index=True)

    # Text context or conversation history payload
    content = Column(Text, nullable=False)

    # Structured transaction data (LangChain Context, Metadata)
    metadata_ = Column("metadata", JSON, default={}, nullable=True)

    # 1536 dimension vector storing embeddings
    embedding = Column(CrossVector)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
