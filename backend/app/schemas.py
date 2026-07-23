from pydantic import BaseModel, EmailStr
from datetime import datetime


# ===================== AUTH =====================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# ===================== RESUME =====================

class ResumeUploadResponse(BaseModel):
    id: int
    file_name: str
    job_title: str
    job_description: str
    score: float
    uploaded_at: datetime

    class Config:
        from_attributes = True


class RecruiterResumeResponse(BaseModel):
    id: int
    file_name: str
    job_title: str
    job_description: str
    score: float
    uploaded_at: datetime
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
