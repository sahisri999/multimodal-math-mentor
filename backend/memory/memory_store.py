from sqlalchemy.orm import Session
from backend.memory.models import Conversation


def store_conversation(db: Session, problem: str, solution: str, explanation: str):

    conversation = Conversation(
        problem=problem,
        solution=solution,
        explanation=explanation
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def retrieve_conversation(db: Session, problem: str):
    """
    Retrieve previously solved problem
    """

    conversation = db.query(Conversation).filter(
        Conversation.problem == problem
    ).first()

    return conversation