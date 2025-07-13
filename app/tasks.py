from app.celery_worker import celery_app
from app.ai.dto import ScreenCommentResult
from app.persistence.comments import persist_comment_screening_result

@celery_app.task
def persist_comment_job(result_dict):
    result = ScreenCommentResult(**result_dict)
    persist_comment_screening_result(result)
    return True