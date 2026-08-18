# Resume Builder & ATS Resume Analyzer

A full-stack **Resume Builder and ATS Resume Analyzer** that allows users to create, upload, and analyze resumes against a job description. The application extracts resume content from PDF/DOCX files, identifies relevant technical skills and keywords, and calculates an ATS compatibility score.

## 🚀 Features

* Create and manage professional resumes
* Upload resumes in **PDF** and **DOCX** format
* Extract text automatically from uploaded resumes
* Extract text from DOCX tables as well as paragraphs
* Analyze resumes against a specific job description
* Identify matching technical skills
* Identify missing skills
* Identify matching and missing keywords
* Calculate an ATS compatibility score from **0–100**
* User authentication and authorization
* Store resume information in a database
* RESTful backend API
* Interactive API documentation with Swagger/OpenAPI
* Secure file upload handling
* Unique filenames for uploaded resumes

## 🧠 ATS Resume Analysis

The application analyzes the uploaded resume against the provided job description.

The scoring system considers:

| Category                 |   Weight |
| ------------------------ | -------: |
| Technical Skill Matching |      60% |
| Keyword Matching         |      40% |
| **Total**                | **100%** |

### Example

**Job Description**

```text
Looking for a Software Engineer with experience in
C#, ASP.NET Core, SQL Server, REST API and Git.
```

**Resume**

```text
Software Engineer

Skills:
C#
ASP.NET Core
SQL Server
Git
JavaScript
```

The analyzer identifies:

### Matched Skills

* C#
* ASP.NET Core
* SQL Server
* Git

### Missing Skills

* REST API

The final ATS score is calculated from the percentage of relevant skills and keywords found in the resume.

## 📄 Supported Resume Formats

The application supports:

* `.pdf`
* `.docx`

For PDF resumes, text is extracted using **PyPDF2**.

For DOCX resumes, the application extracts:

* Normal paragraphs
* Table contents

> Scanned/image-only PDFs are not supported by the standard text extraction process. A text-based PDF or DOCX should be uploaded.

## 🏗️ Project Architecture

```text
ResumeBuilderApp
│
├── backend
│   │
│   ├── app
│   │   ├── routes
│   │   │   └── resume_routes.py
│   │   │
│   │   ├── resume_parser.py
│   │   ├── scoring.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── main.py
│   │
│   ├── uploads
│   ├── requirements.txt
│   └── ...
│
├── frontend
│   ├── ...
│   └── ...
│
└── README.md
```

## 🔄 Application Flow

```text
User
 │
 ▼
Create / Upload Resume
 │
 ▼
Select Job Title
 │
 ▼
Enter Job Description
 │
 ▼
Upload PDF / DOCX
 │
 ▼
Resume Parser
 │
 ├── PDF → PyPDF2
 │
 └── DOCX → python-docx
 │
 ▼
Extract Resume Text
 │
 ▼
ATS Analyzer
 │
 ├── Extract Skills
 │
 ├── Extract Keywords
 │
 ├── Find Matched Skills
 │
 └── Find Missing Skills
 │
 ▼
Calculate ATS Score
 │
 ▼
Store Result in Database
 │
 ▼
Display Score
```

## 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* SQLAlchemy
* PyPDF2
* python-docx
* Pydantic
* Uvicorn

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQL database
* SQLAlchemy ORM

### API Documentation

* Swagger UI
* OpenAPI

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/msrikanta/ResumeBuilderApp.git
```

```bash
cd ResumeBuilderApp
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Navigate to the backend folder:

```bash
cd backend
```

Install the required packages:

```bash
pip install -r requirements.txt
```

If necessary, install the resume-processing packages manually:

```bash
pip install PyPDF2 python-docx
```

## ⚙️ Configuration

Configure your database and application settings according to the project's configuration files.

For example:

```text
DATABASE_URL=your_database_connection_string
```

Do not commit passwords, API keys, or other sensitive credentials to GitHub.

## ▶️ Run the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

## 📚 Swagger API Documentation

Once the backend is running, open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API endpoints.

## 📤 Resume Upload

The resume upload API accepts:

```text
POST /resume/upload
```

The request contains:

```text
job_title
job_description
file
```

### Supported files

```text
.pdf
.docx
```

The API:

1. Validates the file
2. Saves the uploaded resume
3. Extracts resume text
4. Validates extracted content
5. Analyzes skills
6. Analyzes keywords
7. Calculates ATS score
8. Saves the result
9. Returns the score

## 📊 ATS Analysis Result

The analyzer can identify:

```text
ATS Score
Matched Skills
Missing Skills
Matched Keywords
Missing Keywords
Resume Word Count
Job Description Keyword Count
```

Example:

```json
{
  "score": 78.5,
  "matched_skills": [
    "c#",
    "asp.net core",
    "git",
    "sql server"
  ],
  "missing_skills": [
    "docker",
    "azure"
  ]
}
```

## 🔐 Security

The application includes secure practices such as:

* Authentication
* Authorization
* User-specific resume records
* File extension validation
* Safe generated filenames
* Password protection
* Database transaction handling

Uploaded files are assigned unique filenames rather than directly using the original filename.

## 🧪 Testing

After starting the backend:

1. Open Swagger.
2. Authenticate if required.
3. Open the resume upload endpoint.
4. Enter a job title.
5. Enter a detailed job description.
6. Upload a PDF/DOCX resume.
7. Execute the request.
8. Check the returned ATS score.

Check the backend terminal for processing information:

```text
========== RESUME PROCESSING ==========
Extracted characters : 2458
Extracted words      : 382
=======================================

========== ATS ANALYSIS ==========
ATS Score       : 67.42
==================================
```

## ⚠️ Troubleshooting

### Score is 0

First check the backend terminal.

If you see:

```text
Extracted characters : 0
```

the PDF/DOCX parser could not extract readable text.

Try uploading:

* A text-based PDF
* A DOCX file
* A resume generated directly from Word/Google Docs

Avoid scanned image-only PDFs.

### PDF text is not extracted correctly

Some PDFs contain their resume content as images rather than actual text.

`PyPDF2` cannot perform OCR.

Convert the resume to a text-based PDF or DOCX.

### Unsupported file error

Only these extensions are accepted:

```text
.pdf
.docx
```

### ATS score is low

A low score does not necessarily mean the resume is bad.

The score depends on how closely the resume matches the supplied job description.

For better results, the resume should contain relevant:

* Technical skills
* Frameworks
* Programming languages
* Databases
* Tools
* Certifications
* Job-related keywords

## 📁 Important Backend Files

### `resume_parser.py`

Responsible for extracting text from uploaded PDF and DOCX resumes.

```text
PDF
 ↓
PyPDF2
 ↓
Resume Text
```

and:

```text
DOCX
 ↓
python-docx
 ↓
Paragraphs + Tables
 ↓
Resume Text
```

### `scoring.py`

Responsible for:

* Skill extraction
* Keyword extraction
* Skill matching
* Missing skill detection
* ATS score calculation

### `resume_routes.py`

Responsible for:

* Resume upload
* File validation
* File storage
* Text extraction
* ATS analysis
* Database storage
* API response

## 🎯 Future Improvements

The project can be extended with:

* OCR support for scanned resumes
* AI-powered resume analysis
* Resume section detection
* Experience matching
* Education matching
* Job recommendation
* Resume improvement suggestions
* ATS-friendly resume templates
* PDF resume generation
* Resume keyword suggestions
* Skill gap analysis
* Resume ranking
* Multiple job-description comparison
* Dashboard with ATS score history
* Resume version management

## 💼 Resume Project Description

**Resume Builder & ATS Resume Analyzer** — Developed a full-stack resume management application using Python, FastAPI, SQLAlchemy, HTML, CSS and JavaScript that enables users to create/upload resumes and evaluate them against job descriptions. Implemented PDF/DOCX text extraction, technical skill and keyword matching, missing-skill detection, and weighted ATS scoring to provide actionable resume optimization insights.

## 👨‍💻 Author

**Srikanta Mishra**

GitHub:
https://github.com/msrikanta

Repository:
https://github.com/msrikanta/ResumeBuilderApp

## ⭐ Project

If you find this project useful, consider giving the repository a star on GitHub.
