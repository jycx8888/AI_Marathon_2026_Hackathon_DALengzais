<div align="center">

<img src="https://img.shields.io/badge/RecruQ-AI%20Recruitment%20Agent-6366f1?style=for-the-badge&logo=robot&logoColor=white"/>

<h1>RecruQ 🤖</h1>
<h3>AI-Powered Intelligent Recruitment Agent</h3>
<p><em>Bridging diverse talent and hiring managers through intelligent automation</em></p>

<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gradio-UI-FF7C00?style=flat-square&logo=gradio&logoColor=white"/>
  <img src="https://img.shields.io/badge/Morpheus_AI-llama--3.3--70b-6366f1?style=flat-square"/>
  <img src="https://img.shields.io/badge/Gmail-SMTP-EA4335?style=flat-square&logo=gmail&logoColor=white"/>
  <img src="https://img.shields.io/badge/Hackathon-AI_Marathon_2026-22c55e?style=flat-square"/>
</p>

<p>Built for <strong>AI Marathon 2026 Hackathon</strong> · Team DA Lengzais</p>

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the App](#-running-the-app)
- [How to Use](#-how-to-use)
- [Testing the Email Feature](#-testing-the-email-feature)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Common Issues](#-common-issues)

---

## 🌟 Overview

**RecruQ** is an agentic AI recruitment system that takes a job description and a pool of candidate profiles, then uses **Morpheus AI** to intelligently rank candidates by match score, generate personalised outreach emails, and maintain a searchable history of past searches — all through a clean web interface.

> **Agentic AI design:** RecruQ follows a Perceive → Reason → Act pipeline. The LLM evaluates candidates, drafts personalised emails, and dispatches outreach — with a human-in-the-loop review step before any email is sent.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **AI Candidate Ranking** | Scores each candidate 0–100 with strengths, gaps and verdict |
| 📧 **Email Outreach Agent** | AI drafts personalised emails, recruiter reviews before sending |
| 👤 **Full Candidate Profile** | Skills, experience, education, certifications in one popup |
| 🕐 **Search History** | Saves past searches with auto-generated titles, pin up to 3 |
| 📊 **Responsive Card Layout** | Clean grid with score arc circles and match badges |
| ⏳ **Live Progress Overlay** | Real-time progress with elapsed and estimated time |

---

## 🖥️ Prerequisites

Before running RecruQ, make sure you have the following ready:

### 1. Python 3.8 or above

Check your Python version:
```bash
python --version
```

If Python is not installed, download it from [python.org/downloads](https://python.org/downloads).

> ⚠️ **Windows users:** During installation, check **"Add Python to PATH"** before clicking Install — otherwise `python` and `pip` commands won't be recognised in the terminal.

---

### 2. Morpheus AI API Key

1. Sign up at [app.mor.org](https://app.mor.org)
2. Go to your dashboard and generate an API key
3. Keep it ready for the [Configuration](#-configuration) step

---

### 3. Gmail Account + App Password

RecruQ sends emails via Gmail SMTP. You need a **Gmail App Password** (not your regular Gmail password).

**Step-by-step to generate an App Password:**

| Step | Action |
|---|---|
| 1 | Go to [myaccount.google.com](https://myaccount.google.com) |
| 2 | Click **Security** in the left menu |
| 3 | Enable **2-Step Verification** ← must do this first |
| 4 | Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| 5 | Select **Mail** + **Windows Computer**, click **Generate** |
| 6 | Copy the 16-character password (remove spaces when pasting) |

> ⚠️ The App Passwords option **only appears after** 2-Step Verification is turned on. If you don't see it, complete Step 3 first.

---

## ⚙️ Installation

### Step 1 — Download and Extract the ZIP file

### Step 2 — Open the file

### Step 3 — Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install gradio openai python-dotenv
```

> **Not using the local JSON dataset?** If you want to load from Hugging Face instead, also run:
> ```bash
> python -m pip install datasets
> ```

### Step 4 — Verify installation

```bash
python -c "import gradio, openai, dotenv; print('All dependencies installed!')"
```

You should see: `All dependencies installed!`

---

## 🔧 Configuration

### Step 1 — Edit `.env` file

Edit the file named `.env` and fill in your credentials:

```env
MORPHEUS_API_KEY=your_morpheus_api_key_here
GMAIL_USER=youremail@gmail.com
GMAIL_PASSWORD=your16characterapppassword
RECRUITER_NAME=Your Full Name
COMPANY_NAME=Your Company Name
```

> ⚠️ **Important formatting rules for `.env`:**
> - No spaces around `=` → ✅ `KEY=value` &nbsp; ❌ `KEY = value`
> - No quotes around values → ✅ `KEY=abc123` &nbsp; ❌ `KEY="abc123"`
> - App Password: paste without spaces → ✅ `abcdefghijklmnop`

### Step 2 — Add `.env` to `.gitignore`

Make sure your credentials are never accidentally uploaded to GitHub:

```bash
echo ".env" >> .gitignore
```

### Step 3 — Verify dataset file

Make sure `candidates_dataset.json` is in the root project folder.

Your final project structure should look like this:

```
recruq/
├── .env                       ← your credentials (never commit!)
├── .gitignore
├── candidates_dataset.json    ← 50 Malaysian candidate profiles
├── app.py                     ← Gradio web interface
├── agent.py                   ← Morpheus AI ranking logic
├── data_loader.py             ← loads candidate data
├── email_agent.py             ← email generation and sending
├── history_manager.py         ← search history management
├── main.py                    ← terminal version for testing
└── README.md
```

---

## ▶️ Running the App

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:7860
```

> If port `7860` is busy, Gradio will automatically use the next available port and print the URL in the terminal.

---

## 📖 How to Use

### Step 1 — Enter a Job Description

Type or paste a job description into the **📋 Job Description** text box. Include the job title, required skills, years of experience, and any other requirements for the best results.

You can also click any of the **💡 Example Job Descriptions** to instantly load a pre-filled example.

---

### Step 2 — Select Number of Candidates

Use the **👥 slider** to choose how many candidates to analyse:

| Value | Best for |
|---|---|
| 5 | Quick demo or testing |
| 10 | Standard search |
| 15 | Broader talent pool |
| 20 | Maximum coverage |

> More candidates = more accurate ranking but slightly longer processing time.

---

### Step 3 — Click "Find Best Candidates"

Click **🚀 Find Best Candidates**. A loading overlay appears showing live progress:

```
📥 Loading candidate dataset...          10%
✅ Loaded 10 candidates! Sending to AI... 45%
🤖 AI is analyzing and ranking...        65%
📊 Finalizing ranked results...          90%
🎉 Analysis Complete!                   100%
```

> Input fields are **locked** during processing to prevent accidental edits.

---

### Step 4 — Review Ranked Results

Candidates appear as cards ranked from best to worst. Each card shows:

- **Score circle** — match score out of 100
  - 🟢 `70–100` Strong Match
  - 🟡 `40–69` Partial Match
  - 🔴 `0–39` Weak Match
- **✅ Strengths** — top matching qualities found in the resume
- **❌ Gaps** — requirements missing from the candidate's profile
- **💬 Verdict** — one-line hiring recommendation

---

### Step 5 — Contact a Candidate

Click the **📧 Contact** button on any card. A popup appears with two sections:

**Top — Full Candidate Profile:**
- Name, current role, location, years of experience
- Email address, phone number, languages spoken
- Match strengths vs gaps (side by side)
- Skills breakdown by category (technical, tools, soft skills)
- Work experience with company, title, duration, responsibilities
- Education with degree, institution and CGPA
- Certifications

**Bottom — AI-Generated Email (editable):**
1. Morpheus AI automatically drafts a personalised email
2. Edit the **subject line** or **email body** freely if needed
3. Click **📨 Send Email** when satisfied

> ✅ The email is **only sent after you click Send** — you are always in control.

---

### 🧪 Testing the Email Feature

Since the candidate profiles use fictional email addresses, you can test the email sending feature by temporarily replacing one candidate's email with your own.

**Step 1 — Open `candidates_dataset.json`**

Find any candidate entry, for example:

```json
{
  "id": 1,
  "name": "Ahmad Farid bin Zulkifli",
  "email": "ahmad.farid@gmail.com",
  ...
}
```

**Step 2 — Replace the email with your own**

```json
{
  "id": 1,
  "name": "Ahmad Farid bin Zulkifli",
  "email": "youremail@gmail.com",
  ...
}
```

**Step 3 — Run the app and contact that candidate**

1. Run `python app.py`
2. Enter any job description and click **🚀 Find Best Candidates**
3. Find the candidate whose email you changed (e.g. Ahmad Farid)
4. Click **📧 Contact** on their card
5. Review the AI-generated email in the popup
6. Click **📨 Send Email**
7. Check your inbox — the personalised email should arrive within seconds

> ✅ If the email arrives successfully, your Gmail credentials are correctly configured and the full email agent pipeline is working.
>
> 💡 **Remember to revert the email address back** after testing so the dataset stays accurate for the actual demo.

**Verify send without UI (optional terminal test):**
```bash
python -c "from email_agent import send_email; result = send_email('youremail@gmail.com', 'RecruQ Test', 'Email agent is working!'); print('Success!' if result else 'Failed!')"
```

---

### 🧪 Testing the Email Feature

Since the candidate profiles use fictional email addresses, you can test the email sending feature by temporarily replacing one candidate's email with your own.

**Step 1 — Open `candidates_dataset.json`**

Find any candidate entry, for example:

```json
{
  "id": 1,
  "name": "Ahmad Farid bin Zulkifli",
  "email": "ahmad.farid@gmail.com",
  ...
}
```

**Step 2 — Replace the email with your own**

```json
{
  "id": 1,
  "name": "Ahmad Farid bin Zulkifli",
  "email": "youremail@gmail.com",
  ...
}
```

**Step 3 — Run the app and contact that candidate**

1. Run `python app.py`
2. Enter any job description and click **🚀 Find Best Candidates**
3. Find the candidate whose email you changed (e.g. Ahmad Farid)
4. Click **📧 Contact** on their card
5. Review the AI-generated email in the popup
6. Click **📨 Send Email**
7. Check your inbox — the personalised email should arrive within seconds

> ✅ If the email arrives successfully, your Gmail credentials are correctly configured and the full email agent pipeline is working.
>
> 💡 **Remember to revert the email address back** after testing so the dataset stays accurate for the actual demo.

**Verify send without UI (optional terminal test):**
```bash
python -c "from email_agent import send_email; result = send_email('youremail@gmail.com', 'RecruQ Test', 'Email agent is working!'); print('Success!' if result else 'Failed!')"
```

---

### Step 6 — Use Search History

The **🕐 Search History** section above the examples saves your past searches automatically:

| Action | How |
|---|---|
| Load a past search | Click any history item |
| Pin a favourite | Click 🤍 (turns ❤️) |
| Unpin | Click ❤️ again |
| Max pinned items | 3 items only |

> 📌 Pinned searches appear at the top with a **purple background** and persist even after closing the app.
>
> ⚠️ A warning message appears if you try to like a 4th item — unlike one first.

---

## 🗂️ Project Structure

| File | Purpose |
|---|---|
| `app.py` | Main Gradio web interface — UI, layout, all event handling |
| `agent.py` | Morpheus AI integration — candidate ranking + job title generation |
| `data_loader.py` | Loads and formats candidates from `candidates_dataset.json` |
| `email_agent.py` | Generates personalised email via AI, sends via Gmail SMTP |
| `history_manager.py` | Manages search history — save, like, recall, persist |
| `main.py` | Terminal-only version for quick backend testing |
| `candidates_dataset.json` | 50 Malaysian profiles across tech and business roles |
| `history.json` | Auto-created on first search — stores your search history |
| `.env` | API keys and credentials — **never commit this file** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Morpheus AI `llama-3.3-70b` via OpenAI-compatible API |
| Web UI | Gradio |
| Backend | Python 3.8+ |
| Email delivery | Gmail SMTP |
| Candidate data | Custom Malaysian dataset (JSON, 50 profiles) |
| History storage | Local JSON persistent file |
| Prompt strategy | Role-based system prompts + structured JSON output |

---

## 🐛 Common Issues

<details>
<summary><strong>❌ `pip` is not recognised on Windows</strong></summary>

Use `python -m pip` instead:
```bash
python -m pip install gradio openai python-dotenv
```
</details>

<details>
<summary><strong>❌ API key error / missing credentials</strong></summary>

- Make sure `.env` is in the **same folder** as `app.py`
- No spaces around `=` → `KEY=value` not `KEY = value`
- No quotes around values → `KEY=abc123` not `KEY="abc123"`
- Try printing your key to debug: add `print(os.getenv("MORPHEUS_API_KEY"))` at the top of `main.py`
</details>

<details>
<summary><strong>❌ Email not sending</strong></summary>

- Make sure **2-Step Verification** is enabled on your Gmail first
- App Password must be pasted **without spaces**
- Check your **Gmail Sent folder** — if the email appears there, it sent successfully even if it landed in spam
- Try the terminal test first:
```bash
python -c "from email_agent import send_email; print(send_email('test@gmail.com', 'Test', 'Hello!'))"
```
</details>

<details>
<summary><strong>❌ `candidates_dataset.json` not found</strong></summary>

Make sure the file is in the **same folder** as `app.py`, not inside a subfolder. Run this to check:
```bash
ls        # Mac/Linux
dir       # Windows
```
You should see `candidates_dataset.json` listed.
</details>

<details>
<summary><strong>❌ Gradio port already in use</strong></summary>

Specify a different port:
```bash
python app.py --server-port 7861
```
Or just let Gradio auto-pick the next available port.
</details>

---

<div align="center">

Built with ❤️ by **Team DA Lengzais** · AI Marathon 2026 Hackathon

<img src="https://img.shields.io/badge/Powered_by-Morpheus_AI-6366f1?style=flat-square"/>
<img src="https://img.shields.io/badge/UI-Gradio-FF7C00?style=flat-square"/>

</div>
