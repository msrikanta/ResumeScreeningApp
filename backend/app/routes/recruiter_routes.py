from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Resume, User
from app.auth import require_recruiter
from app.schemas import RecruiterResumeResponse

router = APIRouter(prefix="/recruiter", tags=["Recruiter"])


@router.get("/resumes", response_model=List[RecruiterResumeResponse])
def get_all_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter)
):
    resumes = db.query(Resume).order_by(Resume.score.desc()).all()

    response = []
    for resume in resumes:
        response.append({
            "id": resume.id,
            "user_id": resume.user_id,
            "file_name": resume.file_name,
            "job_title": resume.job_title,
            "job_description": resume.job_description,
            "score": resume.score,
            "uploaded_at": resume.uploaded_at,
            "username": resume.user.username if resume.user else "",
            "email": resume.user.email if resume.user else ""
        })

    return response
