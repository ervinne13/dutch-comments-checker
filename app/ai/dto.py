from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ScreenCommentJob(BaseModel):
    type: str
    model: Dict[str, Any]
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
