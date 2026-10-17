"""Budget model"""

from sqlalchemy import Column, String, Integer, Float, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class BudgetType(str, Enum):
    """Budget types"""
    TOKEN = "token"
    API_CALL = "api_call"
    MONETARY = "monetary"
    TIME = "time"
    RESOURCE = "resource"


class Budget(Base, TimestampMixin):
    """Budget model"""
    
    __tablename__ = "budgets"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    budget_type = Column(SQLEnum(BudgetType), nullable=False)
    
    # Limits
    limit = Column(Float, nullable=False)
    used = Column(Float, default=0.0, nullable=False)
    
    # Time window (for rate limiting)
    window_seconds = Column(Integer)  # null for one-time budgets
    
    # Rollover configuration
    rollover_enabled = Column(Boolean, default=True)
    
    # Relationships
    agents = relationship("Agent", back_populates="budget")
