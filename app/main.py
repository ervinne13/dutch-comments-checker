from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.http.requests import CommentRequest
from app.ai.comment_processor import screen_comment
from app.tasks import persist_comment_job
from app.http.responses import CheckedCommentResponse, SubjectListItemResponse
from app.persistence.subjects import get_all_subjects_summary
from app.persistence.comments import get_comments_from_subject

app = FastAPI()

MODERATION_API_PREFIXES = [
    "/api/v1/subjects",
    "/api/v1/moderation"
]

class ModerationCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Handle preflight OPTIONS for check_comment
        if request.method == "OPTIONS" and request.url.path == "/api/v1/check_comment":
            response = JSONResponse({})
            response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
            response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response

        response = await call_next(request)
        # Only add CORS for moderation frontend APIs
        if any(request.url.path.startswith(prefix) for prefix in MODERATION_API_PREFIXES):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
        # Allow CORS for check_comment specifically for localhost:5173
        if request.url.path == "/api/v1/check_comment":
            response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
            response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
        return response

app.add_middleware(ModerationCORSMiddleware)

# Integration APIs
@app.post("/api/v1/check_comment")
async def check_comment(request: CommentRequest):
    result = screen_comment(request.comment, request.context, request.subject, request.subject_id)
    persist_comment_job.delay(result.dict())
    return CheckedCommentResponse(result).dict()

# Moderation Frontend APIs
@app.get("/api/v1/subjects")
async def get_subjects():
    subjects = get_all_subjects_summary()
    subjects = [SubjectListItemResponse(row).dict() for row in subjects]
    return JSONResponse(subjects)

@app.get("/api/v1/subjects/{subject_id}/comments")
async def get_subject_comments(subject_id: int):
    comments = get_comments_from_subject(subject_id)
    return JSONResponse(comments)

# Swagger Docs
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()
