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

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50))  # e.g. translation, text-classification, llm
    name = Column(String(100))

class CommentTranslationResult(Base):
    __tablename__ = "comment_translation_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    text_translation = Column(Text)
    context_translation = Column(Text)
    processed_at = Column(DateTime)

class SpamCommentClassification(Base):
    __tablename__ = "spam_comment_classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    spam = Column(Float)
    ham = Column(Float)
    processed_at = Column(DateTime)

class ToxicCommentClassification(Base):
    __tablename__ = "toxic_comment_classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    toxic = Column(Float)
    insult = Column(Float)
    obscene = Column(Float)
    identity_hate = Column(Float)
    severe_toxic = Column(Float)
    threat = Column(Float)
    processed_at = Column(DateTime)

class LLMCommentAnalysis(Base):
    __tablename__ = "llm_comment_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    results = Column(Text)
    remarks = Column(Text)
    processed_at = Column(DateTime)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=True)
    subject_ref = relationship("Subject", back_populates="comments")
    text = Column(Text, nullable=False)
    context = Column(Text, comment="Can be used for things like the article's first paragraph, or another comment that this comment is replying to. Basically our attempt to 'contextualize' this comment")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
