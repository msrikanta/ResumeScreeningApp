import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.schemas import ResumeUploadResponse
from app.auth import require_candidate
from app.resume_parser import extract_text_from_resume
from app.scoring import calculate_ats_score

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ResumeUploadResponse)
def upload_resume(
    job_title: str = Form(...),
    job_description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_candidate)
):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resume_text = extract_text_from_resume(file_path)
        score = calculate_ats_score(resume_text, job_description)

        new_resume = Resume(
            file_name=file.filename,
            resume_text=resume_text,
            job_title=job_title,
            job_description=job_description,
            score=score,
            user_id=current_user.id
        )

        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

        # IMPORTANT: return exactly what the response model expects
        return ResumeUploadResponse(
            id=new_resume.id,
            file_name=new_resume.file_name,
            job_title=new_resume.job_title,
            job_description=new_resume.job_description,
            score=new_resume.score,
            uploaded_at=new_resume.uploaded_at
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")
