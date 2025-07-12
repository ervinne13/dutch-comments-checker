from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ext_id = Column(String(100), unique=True, nullable=True, comment="The user application's subject (article or whatever's the subject of a comment) id")
    text = Column(Text, nullable=False)
    translated = Column(Text)

    comments = relationship("Comment", back_populates="subject_ref")
    __table_args__ = (
        UniqueConstraint('ext_id', name='_extid_uc'),
    )

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=True)
    subject_ref = relationship("Subject", back_populates="comments")
    text = Column(Text, nullable=False)
    translanted_text = Column(Text)
    context = Column(Text, comment="Can be used for things like the article's first paragraph, or another comment that this comment is replying to. Basically our attempt to 'contextualize' this comment")
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
    llm_last_processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
