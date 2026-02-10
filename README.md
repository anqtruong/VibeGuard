# VibeGuard

VibeGuard is a lightweight, security-focused code scanner that analyzes GitHub repositories for insecure patterns and risky practices, with an emphasis on explainability and deterministic results.

VibeGuard uses transparent, rule-based analysis to highlight actionable findings in an easy way so that developers can understand and fix them quickly.

---

## Inspiration

The barrier to building software has never been lower. With the rise of AI tools and “vibecoding,” thousands of new developers are shipping code every day — often without fully understanding security risks.

Five months ago, a student accidentally pushed his Google Cloud API key to GitHub. He thought it was private, but by the time he realized, it was too late. He received a bill for over $55,000. His mistake was just one of many individuals who've had such a mishap.

Vibecoding doesn't just include people who know how to code, it's also people who've never printed a "Hello World!" in their lives. With that in mind, many don’t yet know what insecure patterns look like.

VibeGuard aims to bridge that gap; VibeGuard aims to help identify dangerous patterns before they become costly mistakes.

---

## What It Does

### Scans Public GitHub Repositories

- Accepts a public GitHub repository URL  
- Downloads the repository as a zip archive (via GitHub codeload)  
- Extracts and filters relevant files  
- Applies deterministic security rules  
- Returns structured findings  

**NOTE: We do NOT retain any repository files.**  
All analysis is performed ephemerally, and no potentially exposed secrets are stored.

---

### Displays Findings

Each finding includes:

- Rule ID  
- Severity (low / medium / high)  
- Explanation  
- File location (when applicable)  

---

### Easy-to-Understand UI

See the vulnerability, what type it is, the severity, and where it is! Learn exactly what you need to fix so you can push your best project.

---

## How We Built It

### Frontend

- Node.js  
- Next.js  
- HTML, CSS, JavaScript  

### Backend

- FastAPI  
- Python  

---

## Challenges We Ran Into

- It was our first time using FastAPI and Nodejs, and for some of us, Git  
- It was hard to figure out how to download the zip archive properly  
- Setting up development environments and resolving merge conflicts was challenging at times  

---

## What We Learned

- How to build and structure an API using FastAPI  
- How to create a full-stack application with Next.js  
- How to collaborate effectively using Git and GitHub  

---

## Dependencies

This project uses Next.js for the frontend, and FastAPI for the backend.

### System Requirements

- Node.js (v18+ recommended)  
- Python 3.10+  

---

## Frontend

```bash
cd frontend
npm install
cd vibeguard
npm run dev
```

To test the demo interface directly, navigate to https://localhost:3000/skeleton.html

## Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at http://127.0.0.1:8000
