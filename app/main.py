from fastapi import FastAPI
from app.http.requests import CommentRequest
from app.ai.comment_processor import screen_comment
from app.tasks import persist_comment_job
from app.http.responses import CheckedCommentResponse

app = FastAPI()

@app.post("/api/v1/check_comment")
async def check_comment(request: CommentRequest):
    result = screen_comment(request.comment)
    persist_comment_job.delay(result.dict())
    response = CheckedCommentResponse(result)
    return response.dict()

# Swagger Docs
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()
