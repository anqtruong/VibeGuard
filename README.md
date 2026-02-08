
VibeGuard is a lightweight, security-focused code scanner that analyzes GitHub repositories for insecure patterns and risky practices, with an emphasis on explainability and deterministic results.

VibeGuard uses transparent, rule-based analysis to highlight actionable findings in an easy way so that developers can understand and fix them quickly.


---


**Inspiration**

Interest in building real projects with real-world impact has been higher than ever, and with the rise of AI and vibecoding, the barrier to entry is lower than ever.

Five months ago, a student accidentally pushed his Google Cloud API key to GitHub. He thought it was private, but by the time he realized, it was too late. He received a bill for over $55,000. His mistake was just one of many individuals who've had such a mishap.

Vibecoding doesn't just include people who know how to code, it's also people who've never printed a "Hello World!" in their lives. With that in mind, you'd never expect them to know how to secure the code they generate either. 

VibeGuard aims to bridge that gap; VibeGuard aims to help identify dangerous patterns before they become costly mistakes.

**What It Does**

**Points Out Potential Vulnerabilities:** when you enter the link to your public GitHub repository, VibeGuard scans a zip archive of the repository and highlights potential vulnerabilities. We do NOT retain any files, so your *potentially* exposed secrets are safe and never stored!

**Easy UI:**  See the vulnerability, what type it is, the severity, and where it is! Learn exactly what you need to fix so you can push your best project.

**How We Built It**

**Frontend:**
-Node.js
-Next.js
-HTML, CSS, JavaScript

**Backend**
-FastAPI
-Python

**Challenges We Ran Into**

- It was our first time using FastAPI and Nodejs, and for some of us, Git
- It was hard to figure out how to download the zip archive properly
- Setting up development environments and resolving merge conflicts was challenging at times

**What We Learned**
- How to build and structure an API using FastAPI
- How to create a full-stack application with Next.js
- How to collaborate effectively using Git and GitHub

****

## Dependencies

This project uses Next.js for the frontend, and FastAPI for the backend

### System
- Node.js (v18+ recommended)
- Python 3.10+

cd frontend
npm install
npm run dev

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

