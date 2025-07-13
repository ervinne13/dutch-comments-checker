import logging
from app.ai.dto import ScreenCommentResult
from app.persistence.db import SessionLocal
from app.persistence.models import Subject, Model, Comment, CommentTranslationResult, SpamCommentClassification, ToxicCommentClassification, LLMCommentAnalysis

def persist_job_models(session, jobs):
    """
    Upsert all models used in the jobs list. Returns a dict of {type: model_instance}.
    """
    models = {}
    for job in jobs:
        model_type = job.model.get("type")
        model_name = job.model.get("name")
        model = session.query(Model).filter_by(type=model_type, name=model_name).first()
        if not model:
            model = Model(type=model_type, name=model_name)
            session.add(model)
            session.flush()  # get model.id
        models[model_type] = model
    return models

def persist_subject(session, result: ScreenCommentResult):
    """
    Upsert subject if it's provided, or fetch by subject_id if available.
    """
    # If subject id is provided, we use that directly
    subject_id = getattr(result, 'subject_id', None)
    if subject_id is not None:
        subject = session.query(Subject).filter_by(ext_id=subject_id).first()
        if subject is not None:
            return subject

    # If both are not provided, there's nothing we can do, we'll work on the comment without a subject
    subject_text = getattr(result, 'subject', None)
    if not subject_text:
        return None

    # Otherwise, try to upsert the subject by text.
    subject = session.query(Subject).filter_by(text=subject_text).first()
    if not subject:
        subject = Subject(ext_id=subject_id, text=subject_text)
        session.add(subject)
        session.flush()

    return subject

def persist_comment(session, result: ScreenCommentResult, subject_id):
    """
    Upsert comment by processed text, context, and subject_id. Returns comment instance.
    """
    comment_text = getattr(result, 'text', None)
    context = getattr(result, 'context', None)
    comment = session.query(Comment).filter_by(text=comment_text, context=context, subject_id=subject_id).first()
    if not comment:
        comment = Comment(text=comment_text, context=context, subject_id=subject_id)
        session.add(comment)
        session.flush()
    return comment

def persist_comment_screening_result(result: ScreenCommentResult):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Persisting comment: {result.dict()}")
    session = SessionLocal()
    try:
        subject = persist_subject(session, result)
        subject_id = subject.id if subject else None

        # We can't really reliably proceed if a subject is provided but 
        # we failed to persist it.
        if getattr(result, 'subject', None) and subject_id is None:
            logging.error("Subject text was provided but no subject_id could be resolved/upserted.")
            raise Exception("Subject text provided but no subject_id found after upsert.")

        comment = persist_comment(
            session,
            result,
            subject_id
        )
        if getattr(result, 'jobs', None):
            # TODO: Ehhh, this should be temporary.
            # Ideally we're sure models exist, but we upsert for now
            # at least until we've built the CMS
            models = persist_job_models(session, result.jobs)
        session.commit()
        logging.info("Persistence successful.")
        return True
    except Exception as e:
        session.rollback()
        logging.error(f"Persistence failed: {e}")
        return False
    finally:
        session.close()

