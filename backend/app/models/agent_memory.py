import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

from app.core.database import Base

class AgentMemory(Base):
    """
    Dedicated Hackathon schema fulfilling the 'Agentic Memory' system of record architecture for CockroachDB.
    """
    __tablename__ = "agent_memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(200), nullable=True, index=True)

    # Text context or conversation history payload
    content = Column(Text, nullable=False)

    # Structured transaction data (LangChain Context, Metadata)
    metadata_ = Column("metadata", JSONB, default={}, nullable=True)

    # 1536 dimension vector storing AWS Titan embeddings for Distributed Similarity Mapping
    embedding = Column(Vector(1536))

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
