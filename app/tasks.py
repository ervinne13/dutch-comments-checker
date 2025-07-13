import logging
from app.celery_worker import celery_app
from app.ai.dto import ScreenCommentResult
from app.persistence.comments import persist_comment_screening_result, persist_comment_moderation_result
from app.ai.moderator import moderate_comment_with_llm
from app.http.responses import CheckedCommentResponse

@celery_app.task
def persist_comment_job(result_dict):
    screening_result = ScreenCommentResult(**result_dict)
    comment_id = persist_comment_screening_result(screening_result)
    response = CheckedCommentResponse(screening_result)

    if comment_id is not None:
        if response.flagged_for_moderation:
            logging.info(f"Comment {comment_id} flagged for moderation: {response.flagged_reason}")
            moderation_result = moderate_comment_with_llm(comment_id, screening_result, response.flagged_reason)
            persist_comment_moderation_result(comment_id, moderation_result)
        else:
            logging.info(f"Comment {comment_id} passed screening without flags.")
    else:
        logging.warning("No comment persisted, we can't proceed with possible escalation.")

    return True