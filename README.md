# Resume Builder & ATS Analyzer

A full-stack **Resume Builder and ATS Resume Analyzer** that allows users to create, upload, and analyze resumes against job descriptions.

## Features

* Create and manage resumes
* Upload **PDF/DOCX** resumes
* Extract resume text automatically
* Analyze job-related keywords and technical skills
* Detect matched and missing skills
* Calculate an ATS score from **0–100**
* User authentication and secure file handling
* REST API with Swagger documentation

## Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQL
* **Resume Processing:** PyPDF2, python-docx

## Run Locally

```bash
git clone https://github.com/msrikanta/ResumeBuilderApp.git
cd ResumeBuilderApp/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

## ATS Analysis

The application compares the uploaded resume with the job description and provides:

* ATS Score
* Matched Skills
* Missing Skills
* Matched Keywords
* Missing Keywords

## Author

**Srikanta Mishra**

GitHub: https://github.com/msrikanta
