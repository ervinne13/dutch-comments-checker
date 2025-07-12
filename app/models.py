from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(Text, nullable=False)
    translanted_comment = Column(Text)
    subject = Column(Text)
    translated_subject = Column(Text)
    context = Column(Text)
    translated_context = Column(Text)
    spam = Column(Float)
    ham = Column(Float)
    toxic = Column(Float)
    insult = Column(Float)
    obscene = Column(Float)
    identity_hate = Column(Float)
    severe_toxic = Column(Float)
    threat = Column(Float)
    llm_escalation_results = Column(Text)
    llm_remarks = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
