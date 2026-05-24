from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("MORPHEUS_API_KEY"),
    base_url="https://api.mor.org/api/v1"
)

def rank_candidates(job_description: str, candidates: list) -> list:
    """Send JD + candidates to Morpheus AI and get ranked results."""

    print(f"\n🤖 Analyzing {len(candidates)} candidates with Morpheus AI...")

    prompt = f"""
You are an expert technical recruiter. Analyze the following candidates 
against the job description and rank them from best to worst match.

JOB DESCRIPTION:
{job_description}

CANDIDATES:
{json.dumps([{"id": c["id"], "name": c["name"], "resume": c["resume_text"]} for c in candidates], indent=2)}

For each candidate return:
1. Match score (0-100)
2. Top 3 matching strengths
3. Key gaps (max 2)
4. One-line hiring recommendation

Return ONLY valid JSON, no extra text:
{{
  "ranked_candidates": [
    {{
      "id": 1,
      "name": "...",
      "score": 85,
      "strengths": ["...", "...", "..."],
      "gaps": ["...", "..."],
      "recommendation": "..."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[
            {"role": "system", "content": "You are an expert recruiter. Always respond in valid JSON only, no markdown, no extra text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=3000
    )

    raw = response.choices[0].message.content
    raw = raw.replace("```json", "").replace("```", "").strip()

    result = json.loads(raw)
    return result["ranked_candidates"]