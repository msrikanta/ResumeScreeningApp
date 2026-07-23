from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import auth_routes, resume_routes, recruiter_routes

app = FastAPI(title="ATS Resume Builder API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "ATS Resume Builder API running"}


app.include_router(auth_routes.router)
app.include_router(resume_routes.router)
app.include_router(recruiter_routes.router)
