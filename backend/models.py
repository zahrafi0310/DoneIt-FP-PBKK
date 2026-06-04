from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

class QuestCategory(enum.Enum):
    akademik = "akademik"
    fun_things = "fun_things"
    soft_skill = "soft_skill"
    lifestyle = "lifestyle"

class Difficulty(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class SubmissionStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user")
    accepted_quests = relationship("AcceptedQuest", back_populates="user")


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(Enum(QuestCategory), nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)
    xp_reward = Column(Integer, nullable=False)
    is_limited = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=True)   
    end_date = Column(DateTime, nullable=True)  
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="quest")
    accepted_quests = relationship("AcceptedQuest", back_populates="quest")


class AcceptedQuest(Base):
    __tablename__ = "accepted_quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    accepted_at = Column(DateTime, default=datetime.utcnow)
    is_cancelled = Column(Boolean, default=False)

    user = relationship("User", back_populates="accepted_quests")
    quest = relationship("Quest", back_populates="accepted_quests")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    photo_path = Column(String, nullable=False)      # path file foto bukti
    description = Column(String, nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.pending)
    rejection_reason = Column(String, nullable=True) 
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)   

    user = relationship("User", back_populates="submissions")
    quest = relationship("Quest", back_populates="submissions")