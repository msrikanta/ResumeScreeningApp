import re


def tokenize(text: str):
    if not text:
        return set()
    words = re.findall(r"\b[a-zA-Z0-9+#.]+\b", text.lower())
    return set(words)


def calculate_ats_score(resume_text: str, job_description: str) -> float:
    """
    Very simple ATS scoring:
    score = percentage of JD keywords found in resume
    """
    resume_words = tokenize(resume_text)
    jd_words = tokenize(job_description)

    if not jd_words:
        return 0.0

    matched = resume_words.intersection(jd_words)
    score = (len(matched) / len(jd_words)) * 100
    return round(score, 2)
