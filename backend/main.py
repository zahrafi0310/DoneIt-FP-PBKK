from fastapi import FastAPI
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from database import engine, Base, get_db
import models
from routers import auth, quests, submissions
from sqlalchemy.orm import Session
from auth import get_current_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DoneIt API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(quests.router)
app.include_router(submissions.router)

@app.get("/")
def root():
    return {"message": "DoneIt API is running!"}

@app.get("/admin/stats")
def get_stats(db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    from sqlalchemy import func
    from models import User, Quest, Submission, SubmissionStatus

    active_users = db.query(User).filter(
        User.submissions.any()
    ).count()

    active_quests = db.query(Quest).filter(
        Quest.is_active == True
    ).count()

    total_submissions = db.query(Submission).count()

    approved = db.query(Submission).filter(
        Submission.status == SubmissionStatus.approved
    ).count()

    pending = db.query(Submission).filter(
        Submission.status == SubmissionStatus.pending
    ).count()

    rejected = db.query(Submission).filter(
        Submission.status == SubmissionStatus.rejected
    ).count()

    quests_by_category = db.query(
        Quest.category, func.count(Quest.id)
    ).filter(
        Quest.is_active == True
    ).group_by(Quest.category).all()

    return {
        "active_users": active_users,
        "active_quests": active_quests,
        "total_submissions": total_submissions,
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
        "quests_by_category": {cat.value: count for cat, count in quests_by_category}
    }