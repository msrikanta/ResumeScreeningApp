import re
from typing import Dict, List, Set


# Common words that should NOT be treated as important ATS keywords.
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "by",
    "can", "candidate", "candidates", "do", "does", "for",
    "from", "has", "have", "he", "her", "his", "in", "into",
    "is", "it", "its", "job", "looking", "more", "of", "on",
    "or", "our", "required", "requirements", "role", "should",
    "skills", "that", "the", "their", "them", "these", "this",
    "to", "under", "using", "we", "will", "with", "you", "your",
    "years", "year", "work", "working", "experience", "ability",
    "strong", "good", "knowledge", "including", "preferred",
    "responsibilities", "responsibility", "position", "team",
    "teams", "within", "about", "who", "which", "while", "also",
    "other", "such", "through", "etc"
}


# Common technical skills and technologies.
# Multi-word entries are intentionally included.
KNOWN_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    ".net",
    "dotnet",
    "asp.net",
    "asp.net core",
    "angular",
    "react",
    "react.js",
    "next.js",
    "node.js",
    "node",
    "express",
    "html",
    "css",
    "bootstrap",
    "tailwind",
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "sql server",
    "sqlite",
    "oracle",
    "entity framework",
    "entity framework core",
    "ef core",
    "rest api",
    "restful api",
    "web api",
    "api",
    "git",
    "github",
    "gitlab",
    "docker",
    "kubernetes",
    "azure",
    "aws",
    "gcp",
    "amazon web services",
    "microsoft azure",
    "linux",
    "windows",
    "fastapi",
    "flask",
    "django",
    "spring",
    "spring boot",
    "hibernate",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "power bi",
    "excel",
    "agile",
    "scrum",
    "microservices",
    "jwt",
    "oauth",
    "oauth2",
    "json",
    "xml",
    "linq",
    "async",
    "asyncio",
    "unit testing",
    "testing",
    "selenium",
    "postman",
    "swagger",
    "openapi",
    "visual studio",
    "vs code",
    "figma"
}


def normalize_text(text: str) -> str:
    """
    Normalize text for matching while preserving useful
    technology characters.
    """
    if not text:
        return ""

    text = text.lower()

    # Normalize common variants
    replacements = {
        "asp dot net core": "asp.net core",
        "asp dotnet core": "asp.net core",
        "aspnet core": "asp.net core",
        "microsoft sql server": "sql server",
        "amazon web services": "aws",
        "microsoft azure": "azure",
        "react js": "react.js",
        "node js": "node.js",
        "next js": "next.js",
        "entity framework core": "entity framework",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text: str) -> Set[str]:
    """
    Convert text into useful individual words.
    """
    text = normalize_text(text)

    if not text:
        return set()

    # Keep technical characters such as +, # and .
    words = re.findall(
        r"[a-zA-Z0-9]+(?:[+#.]?[a-zA-Z0-9]+)*",
        text
    )

    return {
        word.lower()
        for word in words
        if word.lower() not in STOP_WORDS
    }


def extract_skills(text: str) -> Set[str]:
    """
    Find known technical skills in text.
    Handles both single-word and multi-word skills.
    """
    normalized = normalize_text(text)

    if not normalized:
        return set()

    found = set()

    for skill in KNOWN_SKILLS:
        # Escape the skill so characters like +, # and . work safely.
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"

        if re.search(pattern, normalized):
            found.add(skill)

    return found


def extract_keywords(job_description: str) -> Set[str]:
    """
    Extract meaningful ATS keywords from the job description.

    Skills are preferred because they are much more useful
    than ordinary English words.
    """
    if not job_description:
        return set()

    skills = extract_skills(job_description)

    words = tokenize(job_description)

    # Add meaningful individual words as secondary keywords.
    # Keep only reasonably useful words.
    words = {
        word
        for word in words
        if len(word) >= 3
    }

    return skills.union(words)


def calculate_ats_score(
    resume_text: str,
    job_description: str
) -> float:
    """
    Calculate a practical ATS-style score from 0-100.

    Weighting:
        60% - technical skill matching
        40% - meaningful keyword matching
    """

    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Resume text is empty. Cannot calculate ATS score."
        )

    if not job_description or not job_description.strip():
        raise ValueError(
            "Job description is empty. Cannot calculate ATS score."
        )

    resume_normalized = normalize_text(resume_text)
    jd_normalized = normalize_text(job_description)

    resume_skills = extract_skills(resume_normalized)
    jd_skills = extract_skills(jd_normalized)

    resume_words = tokenize(resume_normalized)
    jd_words = extract_keywords(jd_normalized)

    # Skill score
    if jd_skills:
        matched_skills = resume_skills.intersection(jd_skills)

        skill_score = (
            len(matched_skills) / len(jd_skills)
        ) * 100
    else:
        skill_score = 0.0

    # General keyword score
    if jd_words:
        matched_words = resume_words.intersection(jd_words)

        keyword_score = (
            len(matched_words) / len(jd_words)
        ) * 100
    else:
        keyword_score = 0.0

    # If the JD contains technical skills, prioritize them.
    if jd_skills:
        final_score = (
            skill_score * 0.60
            + keyword_score * 0.40
        )
    else:
        final_score = keyword_score

    return round(min(max(final_score, 0), 100), 2)


def get_ats_analysis(
    resume_text: str,
    job_description: str
) -> Dict:
    """
    Return detailed ATS analysis for the frontend.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty.")

    resume_normalized = normalize_text(resume_text)
    jd_normalized = normalize_text(job_description)

    resume_skills = extract_skills(resume_normalized)
    jd_skills = extract_skills(jd_normalized)

    matched_skills = sorted(
        resume_skills.intersection(jd_skills)
    )

    missing_skills = sorted(
        jd_skills - resume_skills
    )

    resume_words = tokenize(resume_normalized)
    jd_keywords = extract_keywords(jd_normalized)

    matched_keywords = sorted(
        resume_words.intersection(jd_keywords)
    )

    missing_keywords = sorted(
        jd_keywords - resume_words
    )

    score = calculate_ats_score(
        resume_text,
        job_description
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "resume_text_length": len(resume_text),
        "resume_word_count": len(resume_words),
        "job_keyword_count": len(jd_keywords)
    }

