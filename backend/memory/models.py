from sqlalchemy import Column, Integer, Text, TIMESTAMP,String
from sqlalchemy.sql import func
from backend.memory.db import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    problem = Column(Text)
    solution = Column(Text)
    explanation = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Feedback(Base):

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    problem = Column(Text)

    solution = Column(Text)

    rating = Column(String)

    comment = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

   