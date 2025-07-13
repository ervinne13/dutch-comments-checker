from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AIModel(BaseModel):
    type: str
    name: str

class ScreenCommentJob(BaseModel):
    type: str
    model: AIModel
    # Gonna do Any for now. This kinda grew into allowing more models
    # in one screening instead of fixed spam+toxic only.
    # I'll need to consider making this concrete but I'll opt for 
    # flexibility for now so I can move fast
    output: Any

class ScreenCommentResult(BaseModel):
    subject_id: Optional[str] = None
    subject: Optional[str] = None
    context: Optional[str] = None
    text: str # The actual comment
    jobs: List[ScreenCommentJob]

    @classmethod
    def from_raw(cls, raw):
        jobs = [ScreenCommentJob(**job) for job in raw.get("jobs", [])]
        return cls(processed=raw.get("processed"), jobs=jobs)

class CommentModerationResult(BaseModel):
    comment_id: int
    model: AIModel
    prompt: str
    moderation_decision: str
    classifier_flagged_as: str
    confidence: float
    reasoning: str
