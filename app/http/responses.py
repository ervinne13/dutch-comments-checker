from app.ai.dto import ScreenCommentResult

class CheckedCommentResponse:
    def __init__(self, screened_comment: ScreenCommentResult):
        self.original = screened_comment.text
        self.translation = None
        self.spam = None
        self.toxicity = None
        self.flagged_reason = None
        self.flagged_for_moderation = False
        for job in screened_comment.jobs:
            if job.type == "translation":
                self.translation = job.output.get("translation")
            elif job.type == "spam_classification":
                self.spam = job.output
                if self.spam and self.spam.get("label") == "spam":
                    self.flagged_for_moderation = True
                    self.flagged_reason = "spam"
            elif job.type == "toxicity_classification":
                self.toxicity = job.output
                if self.toxicity:
                    for item in self.toxicity:
                        if item.get("label") == "toxic" and item.get("score", 0) >= 0.3:
                            self.flagged_for_moderation = True
                            self.flagged_reason = "toxic"
                            break

    def dict(self):
        return {
            "original": self.original,
            "translation": self.translation,
            "spam": self.spam,
            "toxicity": self.toxicity,
            "flagged_for_moderation": self.flagged_for_moderation,
            "flagged_reason": self.flagged_reason
        }

class SubjectListItemResponse:
    def __init__(self, row):
        self.id = row.get('id') or row.get('subject_id')
        self.title = row.get('title') or row.get('subject_text')
        self.comment_count = row.get('comment_count') or row.get('total_comment_count')
        self.spam_count = row.get('spam_count') or row.get('spam_comment_count')
        self.toxic_count = row.get('toxic_count') or row.get('toxic_comment_count')

    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'comment_count': self.comment_count,
            'spam_count': self.spam_count,
            'toxic_count': self.toxic_count
        }
