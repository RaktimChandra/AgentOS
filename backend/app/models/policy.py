"""Policy model"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Policy(Base, TimestampMixin):
    """Policy model"""
    
    __tablename__ = "policies"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Policy content (Rego)
    rego_code = Column(Text, nullable=False)
    version = Column(String, default="1.0.0", nullable=False)
    
    # OPA configuration
    opa_path = Column(String, default="agentos/auth")
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    agents = relationship("Agent", back_populates="policy")
