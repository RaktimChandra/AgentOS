"""Replay model for regression testing"""

from sqlalchemy import Column, String, Text, Integer, Float, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class ReplayMode(str, Enum):
    """Replay modes"""
    FULL = "full"  # All boundaries from record
    CUT_POINT = "cut_point"  # Selected boundaries live, rest from record
    LIVE = "live"  # All boundaries live


class ReplayStatus(str, Enum):
    """Replay status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Replay(Base, TimestampMixin):
    """Replay model"""
    
    __tablename__ = "replays"
    
    id = Column(String, primary_key=True, index=True)
    execution_id = Column(String, ForeignKey("executions.id"), nullable=False)
    
    # Replay configuration
    mode = Column(SQLEnum(ReplayMode), default=ReplayMode.FULL, nullable=False)
    cut_points = Column(JSON)  # Array of boundary names to execute live
    
    # Status
    status = Column(SQLEnum(ReplayStatus), default=ReplayStatus.PENDING, nullable=False)
    
    # Results
    output_data = Column(Text)  # JSON output
    duration_seconds = Column(Float)
    
    # Comparison with original
    tools_changed = Column(Boolean, default=False)
    output_changed = Column(Boolean, default=False)
    regression_detected = Column(Boolean, default=False)
    score_delta = Column(Float)
    
    # Fixtures storage path
    fixtures_path = Column(String)
