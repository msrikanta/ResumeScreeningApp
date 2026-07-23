import re


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(job_description: str):
    text = normalize_text(job_description)

    stop_words = {
        "and", "or", "the", "a", "an", "with", "in", "on", "for", "to",
        "of", "we", "are", "is", "be", "as", "at", "by", "from", "this",
        "that", "will", "can", "have", "has", "had", "our", "your"
    }

    words = text.split()
    keywords = []

    for word in words:
        if len(word) >= 2 and word not in stop_words:
            keywords.append(word)

    # remove duplicates while preserving order
    unique_keywords = list(dict.fromkeys(keywords))
    return unique_keywords


def rank_resume(resume_text: str, job_description: str) -> float:
    """
    ATS-style keyword score:
    score = matched_keywords / total_keywords * 100
    """
    if not resume_text or not resume_text.strip():
        return 0.0

    if not job_description or not job_description.strip():
        return 0.0

    resume = normalize_text(resume_text)
    keywords = extract_keywords(job_description)

    if not keywords:
        return 0.0

    matched = 0
    for keyword in keywords:
        if keyword in resume:
            matched += 1

    score = (matched / len(keywords)) * 100
    return round(score, 2)
