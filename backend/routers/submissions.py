from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import Submission, Quest, User, AcceptedQuest, SubmissionStatus
from schemas import SubmissionResponse, SubmissionReview
from auth import get_current_user, get_current_admin
from datetime import datetime
import shutil
import os

router = APIRouter(prefix="/submissions", tags=["submissions"])

UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def calculate_level(xp: int) -> int:
    if xp < 500:
        return 1
    elif xp < 1500:
        return 2
    else:
        return 3


@router.post("/", response_model=SubmissionResponse)
async def submit_quest(
    quest_id: int = Form(...),
    description: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quest = db.query(Quest).filter(Quest.id == quest_id, Quest.is_active == True).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest tidak ditemukan")

    accepted = db.query(AcceptedQuest).filter(
        AcceptedQuest.user_id == current_user.id,
        AcceptedQuest.quest_id == quest_id,
        AcceptedQuest.is_cancelled == False
    ).first()
    if not accepted:
        raise HTTPException(status_code=400, detail="Kamu belum menerima quest ini")

    if quest.is_limited and quest.end_date and datetime.now() > quest.end_date:
        raise HTTPException(status_code=400, detail="Quest sudah melewati deadline")

    existing = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.quest_id == quest_id,
        Submission.status.in_([SubmissionStatus.pending, SubmissionStatus.approved])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Kamu sudah punya submission aktif untuk quest ini")

    file_ext = photo.filename.split(".")[-1]
    filename = f"{current_user.id}_{quest_id}_{datetime.now().timestamp()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    submission = Submission(
        user_id=current_user.id,
        quest_id=quest_id,
        photo_path=file_path,
        description=description,
        status=SubmissionStatus.pending
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/my", response_model=list[SubmissionResponse])
def get_my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).order_by(Submission.submitted_at.desc()).all()


@router.get("/pending", response_model=list[SubmissionResponse])
def get_pending_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return db.query(Submission).filter(
        Submission.status == SubmissionStatus.pending
    ).order_by(Submission.submitted_at.asc()).all()


@router.put("/{submission_id}/review", response_model=SubmissionResponse)
def review_submission(
    submission_id: int,
    review: SubmissionReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission tidak ditemukan")
    if submission.status != SubmissionStatus.pending:
        raise HTTPException(status_code=400, detail="Submission ini sudah direview")

    quest = db.query(Quest).filter(Quest.id == submission.quest_id).first()

    submission.status      = review.status
    submission.reviewed_at = datetime.now()

    if review.status == SubmissionStatus.approved:
        if not review.rejection_reason:
            pass 

        current_xp_row = db.execute(
            text("SELECT xp FROM users WHERE id = :uid"),
            {"uid": submission.user_id}
        ).fetchone()

        current_xp = (current_xp_row[0] or 0) if current_xp_row else 0
        new_xp     = current_xp + quest.xp_reward
        new_level  = calculate_level(new_xp)

        db.execute(
            text("UPDATE users SET xp = :xp, level = :level WHERE id = :uid"),
            {"xp": new_xp, "level": new_level, "uid": submission.user_id}
        )

    elif review.status == SubmissionStatus.rejected:
        if not review.rejection_reason:
            raise HTTPException(status_code=400, detail="Alasan penolakan wajib diisi")
        submission.rejection_reason = review.rejection_reason

    db.commit()
    db.refresh(submission)
    return submission