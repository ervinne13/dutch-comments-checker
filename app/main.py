from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from app.comment_processor import screen_comment

app = FastAPI()

class CommentRequest(BaseModel):    
    subject: str = Field(..., example="De overheid heeft aangekondigd dat de btw volgend jaar wordt verhoogd.")
    context: Optional[str] = Field(None, example="Ik ben het er niet mee eens.")
    comment: str = Field(..., example="Je begrijpt er echt niets van.")

@app.post("/api/v1/check_comment")
async def check_comment(request: CommentRequest):
    result = screen_comment(request.comment)
    return result

# Swagger Docs
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()
