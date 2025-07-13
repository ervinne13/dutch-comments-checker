from pydantic import BaseModel, Field
from typing import Optional

class CommentRequest(BaseModel):    
    subject: str = Field(..., example="De overheid heeft aangekondigd dat de btw volgend jaar wordt verhoogd.")
    # We'll use string here to take into account the possibility of uuids
    subject_id: Optional[str] = Field(None, example="123456")
    context: Optional[str] = Field(None, example="Ik ben het er niet mee eens.")
    comment: str = Field(..., example="Je begrijpt er echt niets van.")