import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.schemas import ResumeUploadResponse
from app.auth import require_candidate
from app.resume_parser import extract_text_from_resume
from app.scoring import calculate_ats_score, get_ats_analysis


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


# Store uploaded resumes inside backend/uploads
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post(
    "/upload",
    response_model=ResumeUploadResponse
)
def upload_resume(
    job_title: str = Form(...),
    job_description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_candidate)
):
    """
    Upload a resume, extract its text and calculate ATS score.
    """

    # ---------------------------------------------------------
    # 1. Validate filename
    # ---------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a resume file."
        )

    original_filename = os.path.basename(file.filename)

    extension = os.path.splitext(
        original_filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    # ---------------------------------------------------------
    # 2. Validate job description
    # ---------------------------------------------------------

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    if not job_title or not job_title.strip():
        raise HTTPException(
            status_code=400,
            detail="Job title cannot be empty."
        )

    # ---------------------------------------------------------
    # 3. Generate a safe unique filename
    # ---------------------------------------------------------

    safe_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        safe_filename
    )

    # ---------------------------------------------------------
    # 4. Save uploaded file
    # ---------------------------------------------------------

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not save uploaded resume: {str(exc)}"
        )

    # ---------------------------------------------------------
    # 5. Extract resume text
    # ---------------------------------------------------------

    try:
        resume_text = extract_text_from_resume(
            file_path
        )

        # IMPORTANT DEBUG INFORMATION
        print("\n========== RESUME PROCESSING ==========")
        print(f"Original file : {original_filename}")
        print(f"Saved file    : {file_path}")
        print(
            f"Extracted characters : {len(resume_text)}"
        )
        print(
            f"Extracted words      : {len(resume_text.split())}"
        )
        print("=======================================\n")

    except ValueError as exc:
        # Remove unusable uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Resume text extraction failed: {str(exc)}"
        )

    # ---------------------------------------------------------
    # 6. Calculate ATS score
    # ---------------------------------------------------------

    try:
        analysis = get_ats_analysis(
            resume_text,
            job_description
        )

        score = analysis["score"]

        print("\n========== ATS ANALYSIS ==========")
        print(f"ATS Score       : {score}")
        print(
            f"Matched skills  : "
            f"{analysis['matched_skills']}"
        )
        print(
            f"Missing skills  : "
            f"{analysis['missing_skills']}"
        )
        print(
            f"Matched keywords: "
            f"{analysis['matched_keywords']}"
        )
        print("==================================\n")

    except ValueError as exc:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"ATS scoring failed: {str(exc)}"
        )

    # ---------------------------------------------------------
    # 7. Save resume to database
    # ---------------------------------------------------------

    try:
        new_resume = Resume(
            file_name=original_filename,
            resume_text=resume_text,
            job_title=job_title.strip(),
            job_description=job_description.strip(),
            score=score,
            user_id=current_user.id
        )

        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

    except Exception as exc:
        db.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Could not save resume to database: {str(exc)}"
        )

    # ---------------------------------------------------------
    # 8. Return existing response model
    # ---------------------------------------------------------

    return ResumeUploadResponse(
        id=new_resume.id,
        file_name=new_resume.file_name,
        job_title=new_resume.job_title,
        job_description=new_resume.job_description,
        score=new_resume.score,
        uploaded_at=new_resume.uploaded_at
    )


