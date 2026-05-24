import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("MORPHEUS_API_KEY"),
    base_url="https://api.mor.org/api/v1"
)

def generate_email_content(candidate: dict, job_description: str) -> dict:
    """Use Morpheus AI to write a personalised outreach email."""

    prompt = f"""
You are a professional recruiter writing a warm, personalised outreach email to a candidate.

JOB DESCRIPTION:
{job_description}

CANDIDATE PROFILE:
Name: {candidate['name']}
Current Role: {candidate['current_role']}
Years of Experience: {candidate['years_experience']}
Location: {candidate['location']}
Match Score: {candidate['score']}/100
Strengths: {', '.join(candidate['strengths'])}

Write a short, professional and friendly recruitment outreach email.
- Address them by first name
- Mention 1-2 of their specific strengths
- Briefly describe the opportunity
- End with a call to action to schedule a call
- Keep it under 150 words

Return ONLY valid JSON:
{{
  "subject": "email subject line here",
  "body": "full email body here"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[
            {"role": "system", "content": "You are a professional recruiter. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    import json
    raw = response.choices[0].message.content
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email via Gmail SMTP."""
    try:
        sender_name = f"{os.getenv('RECRUITER_NAME', 'The Recruiter')} | Human Resources | {os.getenv('COMPANY_NAME', 'Our Company')}"
        sender_email = os.getenv("GMAIL_USER")

        msg = MIMEMultipart()
        msg["From"] = formataddr((sender_name, sender_email))
        msg["To"] = to_email
        msg["Subject"] = subject
        msg["X-Priority"] = "1"
        msg["Importance"] = "High"

        full_body = f"""{body}
--
{os.getenv("RECRUITER_NAME", "The Recruiter")} | Human Resources
{os.getenv("COMPANY_NAME", "Our Company")}
{sender_email}
"""
        msg.attach(MIMEText(full_body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, os.getenv("GMAIL_PASSWORD"))
            server.sendmail(sender_email, to_email, msg.as_string())

        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def contact_candidate(candidate: dict, job_description: str) -> str:
    """Full pipeline: generate personalised email → send it."""
    try:
        email_content = generate_email_content(candidate, job_description)

        success = send_email(
            to_email=candidate["email"],
            subject=email_content["subject"],
            body=email_content["body"]
        )

        if success:
            return f"✅ Email successfully sent to {candidate['name']} at {candidate['email']}"
        else:
            return f"❌ Failed to send email to {candidate['name']}"

    except Exception as e:
        return f"❌ Error: {str(e)}"