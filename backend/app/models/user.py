"""User model"""

from sqlalchemy import Column, String, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class UserRole(str, Enum):
    """User roles"""
    ADMIN = "admin"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    AUDITOR = "auditor"
    VIEWER = "viewer"


class User(Base, TimestampMixin):
    """User model"""
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.DEVELOPER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String)
    team_id = Column(String, index=True)
    
    # Relationships
    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")
