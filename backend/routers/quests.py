from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quest, AcceptedQuest, User
from schemas import QuestCreate, QuestEdit, QuestResponse, AcceptedQuestResponse
from auth import get_current_user, get_current_admin
from datetime import datetime

router = APIRouter(prefix="/quests", tags=["quests"])

@router.post("/", response_model=QuestResponse, status_code=201)
def create_quest(
    data: QuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    quest = Quest(**data.model_dump())
    db.add(quest)
    db.commit()
    db.refresh(quest)
    return quest

@router.put("/{quest_id}", response_model=QuestResponse)
def edit_quest(
    quest_id: int,
    data: QuestEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest tidak ditemukan")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(quest, field, value)

    db.commit()
    db.refresh(quest)
    return quest

@router.delete("/{quest_id}", status_code=204)
def deactivate_quest(
    quest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest tidak ditemukan")
    quest.is_active = False
    db.commit()

@router.get("/", response_model=list[QuestResponse])
def get_all_quests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Quest).filter(Quest.is_active == True).all()

@router.post("/{quest_id}/accept", status_code=201)
def accept_quest(
    quest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quest = db.query(Quest).filter(Quest.id == quest_id, Quest.is_active == True).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest tidak ditemukan")

    already = db.query(AcceptedQuest).filter(
        AcceptedQuest.user_id == current_user.id,
        AcceptedQuest.quest_id == quest_id,
        AcceptedQuest.is_cancelled == False
    ).first()
    if already:
        raise HTTPException(status_code=400, detail="Quest sudah kamu terima sebelumnya")

    accepted = AcceptedQuest(user_id=current_user.id, quest_id=quest_id)
    db.add(accepted)
    db.commit()
    return {"message": "Quest berhasil diterima!"}

@router.post("/{quest_id}/cancel", status_code=200)
def cancel_quest(
    quest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accepted = db.query(AcceptedQuest).filter(
        AcceptedQuest.user_id == current_user.id,
        AcceptedQuest.quest_id == quest_id,
        AcceptedQuest.is_cancelled == False
    ).first()
    if not accepted:
        raise HTTPException(status_code=404, detail="Kamu belum menerima quest ini")

    accepted.is_cancelled = True
    db.commit()
    return {"message": "Quest berhasil dibatalkan"}

@router.get("/my", response_model=list[AcceptedQuestResponse])
def get_my_quests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accepted = db.query(AcceptedQuest).filter(
        AcceptedQuest.user_id == current_user.id,
        AcceptedQuest.is_cancelled == False
    ).order_by(AcceptedQuest.accepted_at.asc()).all()

    def sort_key(aq):
        if aq.quest.is_limited and aq.quest.end_date:
            return (0, aq.quest.end_date)
        return (1, datetime.max)

    return sorted(accepted, key=sort_key)