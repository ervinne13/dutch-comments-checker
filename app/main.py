from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.comment_processor import process_comment

app = FastAPI()

class CommentRequest(BaseModel):
    comment: str

@app.post("/check")
async def check_comment(request: CommentRequest):
    result = process_comment(request.comment)
    return result
