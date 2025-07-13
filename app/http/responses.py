from app.ai.dto import ScreenCommentResult

class CheckedCommentResponse:
    def __init__(self, screened_comment: ScreenCommentResult):
        self.original = screened_comment.processed
        self.translated = None
        self.spam = None
        self.toxicity = None
        for job in screened_comment.jobs:
            if job.type == "translation":
                self.translated = job.output.get("translation_text")
            elif job.type == "spam_classification":
                self.spam = job.output
            elif job.type == "toxicity_classification":
                self.toxicity = job.output

    def dict(self):
        return {
            "original": self.original,
            "translated": self.translated,
            "spam": self.spam,
            "toxicity": self.toxicity
        }
