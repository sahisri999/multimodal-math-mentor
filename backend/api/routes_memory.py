from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.memory.db import SessionLocal
from backend.memory.memory_store import store_conversation

router = APIRouter(prefix="/memory", tags=["memory"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/store")
def store_memory(data: dict, db: Session = Depends(get_db)):

    problem = data["problem"]
    solution = ", ".join(data["solution"])
    explanation = data["explanation"]

    store_conversation(db, problem, solution, explanation)

    return {"status": "stored"}

from backend.memory.memory_query import get_all_conversations


@router.get("/history")
def get_memory(db: Session = Depends(get_db)):

    conversations = get_all_conversations(db)

    return [
        {
            "id": c.id,
            "problem": c.problem,
            "solution": c.solution,
            "explanation": c.explanation,
            "created_at": c.created_at
        }
        for c in conversations
    ]