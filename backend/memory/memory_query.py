from sqlalchemy.orm import Session
from backend.memory.models import Conversation


def get_all_conversations(db: Session):
    """
    Retrieve all stored math conversations
    """
    return db.query(Conversation).all()


def get_recent_conversations(db: Session, limit: int = 10):
    """
    Retrieve most recent solved problems
    """
    return (
        db.query(Conversation)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
        .all()
    )