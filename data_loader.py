import json

def flatten_resume(candidate: dict) -> str:
    parts = []

    if candidate.get("summary"):
        parts.append(f"SUMMARY: {candidate['summary']}")

    if candidate.get("skills"):
        skills = candidate["skills"]
        for category, items in skills.items():
            if isinstance(items, list) and items:
                parts.append(f"SKILLS - {category.upper()}: {', '.join(items)}")

    if candidate.get("experience"):
        parts.append("EXPERIENCE:")
        for exp in candidate["experience"]:
            parts.append(f"  - {exp.get('title')} at {exp.get('company')} ({exp.get('duration', '')})")
            for r in exp.get("responsibilities", [])[:2]:
                parts.append(f"    • {r}")

    if candidate.get("education"):
        parts.append("EDUCATION:")
        for edu in candidate["education"]:
            parts.append(f"  - {edu.get('degree')} in {edu.get('field')} from {edu.get('institution')} — CGPA: {edu.get('cgpa')}")

    if candidate.get("certifications"):
        parts.append(f"CERTIFICATIONS: {', '.join(candidate['certifications'])}")

    if candidate.get("languages"):
        parts.append(f"LANGUAGES: {', '.join(candidate['languages'])}")

    return "\n".join(parts)


def prepare_candidates(limit=15):
    print("📥 Loading dataset from local JSON...")

    with open("candidates_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    candidates = []
    for candidate in data["candidates"][:limit]:
        candidates.append({
            "id": candidate["id"],
            "name": candidate["name"],
            "current_role": candidate["current_role"],
            "years_experience": candidate["years_experience"],
            "location": candidate.get("location", "Malaysia"),
            "email": candidate.get("email", ""),
            "phone": candidate.get("phone", ""),
            "summary": candidate.get("summary", ""),
            "education": candidate.get("education", []),
            "experience": candidate.get("experience", []),
            "skills": candidate.get("skills", {}),
            "certifications": candidate.get("certifications", []),
            "languages": candidate.get("languages", []),
            "resume_text": flatten_resume(candidate)
        })

    print(f"✅ Loaded {len(candidates)} candidates")
    return candidates