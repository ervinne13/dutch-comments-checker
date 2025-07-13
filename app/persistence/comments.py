import logging
from datetime import datetime, timezone
from app.ai.dto import ScreenCommentResult
from app.persistence.db import SessionLocal
from app.persistence.models import Subject, Model, Comment, CommentTranslationResult, SpamCommentClassification, ToxicCommentClassification, CommentModerationResult
from app.ai.dto import CommentModerationResult as CommentModerationResultDTO

def persist_job_models(session, jobs):
    """
    Upsert all models used in the jobs list. Returns a dict of {type: model_instance}.
    """
    models = {}
    for job in jobs:
        model_type = job.model.type
        model_name = job.model.name
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
        logging.info(f"Saved new subject: ({subject.id}) {subject_text}")
    else:
        # If subject exists but has no ext_id, and result has subject_id, update ext_id
        if not subject.ext_id and subject_id:
            subject.ext_id = subject_id
            session.flush()
            logging.info(f"Updated subject ({subject.id}) ext_id to {subject_id}")

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

        logging.info(f"Saved new comment: {comment_text}")

    return comment

def persist_spam_classification(session, job, model_id, comment_id):
    """
    Persist or update a spam classification job result.
    """
    output = job.output or {}

    label = output.get('label')
    score = output.get('score')

    classification = session.query(SpamCommentClassification).filter_by(model_id=model_id, comment_id=comment_id).first()
    if classification:
        classification.spam = score if label == 'spam' else 0
        classification.ham = score if label == 'ham' else 0
        session.flush()
        
        logging.info(f"Updated spam classification for comment {comment_id} as {label}: {score}")
    else:
        classification = SpamCommentClassification(
            model_id=model_id,
            comment_id=comment_id,
            spam=score if label == 'spam' else 0,
            ham=score if label == 'ham' else 0
        )
        session.add(classification)
        session.flush()

        logging.info(f"Comment {comment_id} classified as {label}: {score}")
    return classification

def get_label_score(output, label):
    for item in output:
        if item.get("label") == label:
            return item.get("score")
    return None

def persist_toxic_classification(session, job, model_id, comment_id):
    """
    Persist or update a toxic classification job result.
    """
    output = job.output or []
    toxicity = get_label_score(output, "toxic")
    insult = get_label_score(output, "insult")
    obscene = get_label_score(output, "obscene")
    identity_hate = get_label_score(output, "identity_hate")
    severe_toxic = get_label_score(output, "severe_toxic")
    threat = get_label_score(output, "threat")
    type = "non toxic"
    if toxicity and toxicity > 0:
        type = "toxic"

    classification = session.query(ToxicCommentClassification).filter_by(model_id=model_id, comment_id=comment_id).first()
    if classification:
        classification.toxic = toxicity
        classification.insult = insult
        classification.obscene = obscene
        classification.identity_hate = identity_hate
        classification.severe_toxic = severe_toxic
        classification.threat = threat
        session.flush()
        logging.info(f"Updated toxicity classification for comment {comment_id} as {type}: {toxicity}")
    else:
        classification = ToxicCommentClassification(
            model_id=model_id,
            comment_id=comment_id,
            toxic=toxicity,
            insult=insult,
            obscene=obscene,
            identity_hate=identity_hate,
            severe_toxic=severe_toxic,
            threat=threat
        )
        session.add(classification)
        session.flush()
        logging.info(f"Comment {comment_id} classified as {type}: {toxicity}")
    return classification

def persist_translation_result(session, job, model_id, comment_id):
    """
    Persist or update a translation job result.
    """
    output = job.output or {}
    text_translation = output.get('translation')
    context_translation = output.get('context_translation', None)
    tranlation = session.query(CommentTranslationResult).filter_by(model_id=model_id, comment_id=comment_id).first()
    if tranlation:
        tranlation.text_translation = text_translation
        tranlation.context_translation = context_translation
        session.flush()
        logging.info(f"Updated translation for comment {comment_id} to {text_translation}")
    else:
        tranlation = CommentTranslationResult(
            model_id=model_id,
            comment_id=comment_id,
            text_translation=text_translation,
            context_translation=context_translation
        )
        session.add(tranlation)
        session.flush()
        logging.info(f"Comment {comment_id} translated to {text_translation}")
    return tranlation

def persist_jobs(session, comment_id: int, result: ScreenCommentResult):
    # TODO persist_job_models should be temporary.
    # Ideally we're sure models exist, but we upsert for now
    # at least until we've built the CMS
    models = persist_job_models(session, result.jobs)
    for job in result.jobs:
        model_type = job.type.lower()
        model = models.get(model_type)
        model_id = model.id if model else None
        match model_type:
            case "spam_classification":
                persist_spam_classification(session, job, model_id, comment_id)
            case "toxicity_classification":
                persist_toxic_classification(session, job, model_id, comment_id)
            case "translation":
                persist_translation_result(session, job, model_id, comment_id)
            case _:
                logging.warning(f"Unknown job type: {model_type}")

def persist_comment_screening_result(result: ScreenCommentResult):
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
            persist_jobs(session, comment.id, result)

        session.commit()
        logging.info("Persistence successful.")
        return comment.id if comment else None
    except Exception as e:
        session.rollback()
        logging.error(f"Persistence failed: {e}")
        return None
    finally:
        session.close()

def persist_comment_moderation_result(comment_id, result: CommentModerationResultDTO):
    """
    Upsert a CommentModerationResult DTO to the comment_moderation_results table.
    If a moderation result for the same comment and model exists, update it. Otherwise, insert a new one.
    """
    session = SessionLocal()
    try:
        # Upsert model
        model_type = result.model.type
        model_name = result.model.name
        model = session.query(Model).filter_by(type=model_type, name=model_name).first()
        if not model:
            model = Model(type=model_type, name=model_name)
            session.add(model)
            session.flush()

        # Upsert moderation result
        moderation = session.query(CommentModerationResult).filter_by(
            model_id=model.id,
            comment_id=comment_id
        ).first()
        if moderation:
            moderation.prompt = result.prompt
            moderation.reasoning = result.reasoning
            moderation.classifier_flagged_as = result.classifier_flagged_as
            moderation.recommended_action = result.moderation_decision
            moderation.confidence = result.confidence
            moderation.processed_at = datetime.now(timezone.utc)
            session.flush()
            logging.info(f"Updated moderation result for comment {comment_id}")
        else:
            moderation = CommentModerationResult(
                model_id=model.id,
                comment_id=comment_id,
                prompt=result.prompt,
                reasoning=result.reasoning,
                classifier_flagged_as=result.classifier_flagged_as,
                recommended_action=result.moderation_decision,
                confidence=result.confidence,
                processed_at=datetime.now(timezone.utc)
            )
            session.add(moderation)
            session.flush()
            logging.info(f"Saved moderation result for comment {comment_id}")
        session.commit()
        return moderation
    except Exception as e:
        session.rollback()
        logging.error(f"Failed to persist moderation result: {e}")
        return None
    finally:
        session.close()