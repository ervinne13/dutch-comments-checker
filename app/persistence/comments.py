import logging
from app.ai.dto import ScreenCommentResult

def persist_comment(result: ScreenCommentResult):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"asdasdfasdfsfa: {result.dict()}")

    # TODO

    return True
