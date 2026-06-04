from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class SubmissionStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class QuestCategory(str, Enum):
    akademik = "akademik"
    fun_things = "fun_things"
    soft_skill = "soft_skill"
    lifestyle = "lifestyle"

class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class SubmissionCreate(BaseModel):
    quest_id: int
    description: str

class SubmissionReview(BaseModel):
    status: SubmissionStatus
    rejection_reason: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    quest_id: int
    photo_path: str
    description: str
    status: SubmissionStatus
    rejection_reason: Optional[str] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class QuestCreate(BaseModel):
    title: str
    description: str
    category: QuestCategory
    difficulty: Difficulty
    xp_reward: int
    is_limited: bool = False
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class QuestEdit(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[QuestCategory] = None
    difficulty: Optional[Difficulty] = None
    xp_reward: Optional[int] = None
    is_limited: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class QuestResponse(BaseModel):
    id: int
    title: str
    description: str
    category: QuestCategory
    difficulty: Difficulty
    xp_reward: int
    is_limited: bool
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class StatsSummary(BaseModel):
    active_users: int
    active_quests: int
    total_submissions: int
    approved_count: int
    pending_count: int
    rejected_count: int

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    xp: int
    level: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AcceptedQuestResponse(BaseModel):
    id: int
    quest_id: int
    accepted_at: datetime
    is_cancelled: bool
    quest: QuestResponse          

    class Config:
        from_attributes = True