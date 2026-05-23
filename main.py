import os
from dotenv import load_dotenv

load_dotenv()
print("API KEY:", os.getenv("MORPHEUS_API_KEY"))  # should print your key

from data_loader import prepare_candidates
from agent import rank_candidates

# ── 1. Define your Job Description ──────────────────────────────
job_description = """
Job Title: DevOps Engineer

Requirements:
- Experience with CI/CD pipelines
- Docker and Kubernetes
- AWS or Azure cloud platforms
- Linux system administration
- Scripting with Bash or Python
- Monitoring tools like Grafana or Prometheus
"""

# ── 2. Load candidates from Hugging Face ────────────────────────
candidates = prepare_candidates(limit=10)  # start with 10 for speed

# ── 3. Run the AI recruiter agent ───────────────────────────────
ranked = rank_candidates(job_description, candidates)

# ── 4. Display results ──────────────────────────────────────────
print("\n" + "="*50)
print("🏆 RANKED CANDIDATES")
print("="*50)

for i, c in enumerate(ranked):
    print(f"\n#{i+1} {c['name']} — Score: {c['score']}/100")
    print(f"  ✅ Strengths : {', '.join(c['strengths'])}")
    print(f"  ❌ Gaps      : {', '.join(c['gaps'])}")
    print(f"  💬 Verdict   : {c['recommendation']}")

print("\n" + "="*50)
print(f"✅ Done! Best candidate: {ranked[0]['name']} ({ranked[0]['score']}/100)")