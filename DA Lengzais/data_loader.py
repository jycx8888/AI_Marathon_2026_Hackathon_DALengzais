from datasets import load_dataset

def flatten_resume(resume: dict) -> str:
    """Convert structured resume JSON into readable text for the LLM."""
    parts = []

    if resume.get("summary"):
        parts.append(f"SUMMARY: {resume['summary']}")

    if resume.get("skills"):
        skills = resume["skills"]
        if isinstance(skills, dict):
            for category, items in skills.items():
                if isinstance(items, list):
                    # Handle list of strings
                    str_items = []
                    for item in items:
                        if isinstance(item, str):
                            str_items.append(item)
                        elif isinstance(item, dict):
                            # Extract any string values from the dict
                            str_items.extend([str(v) for v in item.values() if v])
                    if str_items:
                        parts.append(f"SKILLS - {category.upper()}: {', '.join(str_items)}")
        elif isinstance(skills, list):
            str_skills = []
            for item in skills:
                if isinstance(item, str):
                    str_skills.append(item)
                elif isinstance(item, dict):
                    str_skills.extend([str(v) for v in item.values() if v])
            if str_skills:
                parts.append(f"SKILLS: {', '.join(str_skills)}")

    if resume.get("experience"):
        parts.append("EXPERIENCE:")
        for exp in resume["experience"][:3]:
            if isinstance(exp, dict):
                title = exp.get("title", "")
                company = exp.get("company", "")
                duration = exp.get("duration", "")
                parts.append(f"  - {title} at {company} ({duration})")
                responsibilities = exp.get("responsibilities", [])
                if responsibilities and isinstance(responsibilities, list):
                    # Handle if responsibilities are strings or dicts
                    for r in responsibilities[:2]:
                        if isinstance(r, str):
                            parts.append(f"    • {r}")
                        elif isinstance(r, dict):
                            parts.append(f"    • {' '.join(str(v) for v in r.values() if v)}")

    if resume.get("education"):
        parts.append("EDUCATION:")
        for edu in resume["education"]:
            if isinstance(edu, dict):
                degree = edu.get("degree", "")
                institution = edu.get("institution", "")
                parts.append(f"  - {degree} from {institution}")

    return "\n".join(parts)


def prepare_candidates(limit=15):
    """Load candidates from Hugging Face dataset."""
    print("📥 Loading dataset from Hugging Face...")
    dataset = load_dataset("datasetmaster/resumes", split="train")

    # Debug: print first row keys so we know the structure
    first_row = dataset[0]
    print(f"📋 Dataset columns: {list(first_row.keys())}")

    candidates = []
    for i, row in enumerate(dataset):
        if i >= limit:
            break

        resume_text = flatten_resume(row)

        # Skip if resume text is too short (bad data)
        if len(resume_text) < 50:
            continue

        candidate = {
            "id": i + 1,
            "name": row.get("name", f"Candidate {i + 1}"),
            "resume_text": resume_text
        }
        candidates.append(candidate)

    print(f"✅ Loaded {len(candidates)} candidates")
    return candidates