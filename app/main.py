from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.comment_processor import screen_comment

app = FastAPI()

class CommentRequest(BaseModel):
    comment: str = Field(..., example="Je bent dom")

@app.post("/check")
async def check_comment(request: CommentRequest):
    result = screen_comment(request.comment)
    return result

# Swagger Docs
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()
