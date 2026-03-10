from fastapi import APIRouter
from pydantic import BaseModel
from backend.memory.db import SessionLocal
from backend.memory.models import Feedback

router = APIRouter()


class FeedbackRequest(BaseModel):

    problem: str
    solution: str
    rating: str
    comment: str = ""


@router.post("/feedback")

def submit_feedback(data: FeedbackRequest):

    db = SessionLocal()

    feedback = Feedback(
        problem=data.problem,
        solution=data.solution,
        rating=data.rating,
        comment=data.comment
    )

    db.add(feedback)
    db.commit()

    return {"status": "feedback stored"}