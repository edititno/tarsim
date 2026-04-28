# Tarsim — AI Resume Tailoring Tool

**Tarsim** (ترسیم) — Persian for "sketch" or "draw" — sketches the perfect resume for each role.

An AI-powered tool that builds resumes from scratch, analyzes existing ones, tailors them to specific job descriptions, and searches jobs across LinkedIn, Indeed, Glassdoor, and ZipRecruiter through a single boolean query.

## Live Demo

**Backend API:** [https://web-production-c2db3.up.railway.app](https://web-production-c2db3.up.railway.app)

**Interactive API docs:** [https://web-production-c2db3.up.railway.app/docs](https://web-production-c2db3.up.railway.app/docs)

## What It Does

1. **Build resume from scratch** — answer questions, AI writes a professional ATS-friendly resume
2. **Analyze existing resume** — upload PDF, get strengths/weaknesses/improvement suggestions with score
3. **Tailor to specific jobs** — upload PDF + paste job description, get tailored version + custom cover letter
4. **Find matching jobs** — boolean search across LinkedIn, Indeed, Glassdoor, ZipRecruiter through Google
5. **Export as Word** — download generated content as .docx for editing

## API Endpoints

- `GET /` — API info and version
- `POST /analyze-resume` — Upload PDF, get analysis
- `POST /tailor-resume` — Upload PDF + job description, get tailored resume + cover letter
- `GET /search-jobs?query=&location=` — Boolean job search across major job boards
- `POST /build-resume` — Build resume from structured input
- `POST /export-docx` — Convert text to downloadable Word document

## Tech Stack

- **FastAPI** — Python backend serving all endpoints
- **OpenAI GPT-4o-mini** — Resume analysis, tailoring, building, cover letter generation
- **pdfplumber** — PDF text extraction
- **python-docx** — Word document generation
- **SerpAPI** — Boolean job search via Google across LinkedIn, Indeed, Glassdoor, ZipRecruiter
- **Railway** — Cloud deployment with auto-deploy from GitHub main branch
- **Python** — Backend language

## Why "Boolean Search"

Job search APIs like LinkedIn, Indeed, and Glassdoor are closed or restricted. Most resume tools can't search these directly. Tarsim uses Google's API with site-specific operators to legally surface jobs from all major boards in one query, giving users a unified search across platforms that paid tools typically can't reach for free.

## Architecture

    User PDF/Input
         ↓
    FastAPI Backend (Railway)
         ↓
    ├─ pdfplumber (text extraction)
    ├─ OpenAI API (analysis, tailoring, generation)
    ├─ SerpAPI (boolean job search)
    └─ python-docx (Word export)
         ↓
    Structured JSON / DOCX response

## Run Locally

    git clone https://github.com/edititno/tarsim.git
    cd tarsim
    pip install -r requirements.txt
    uvicorn api.tarsim_api:app --reload

Server runs at `http://localhost:8000`. Docs at `/docs`.

## File Structure

    tarsim/
    ├── api/
    │   └── tarsim_api.py
    ├── .gitignore
    ├── LICENSE
    ├── Procfile
    ├── README.md
    └── requirements.txt

## Roadmap

- React frontend with clean UI (replaces Swagger)
- Vercel deployment for frontend
- PDF export (Word export currently working)
- Application tracking dashboard
- Save and reuse multiple resume versions

## About

Tarsim was built as a portfolio project demonstrating AI engineering skills: API integration, LLM workflows, document processing, and cloud deployment. Part of a series of context-intelligence projects rooted in Persian linguistic concepts.

The name "Tarsim" (ترسیم) is the Persian word for "sketch" or "drawing" — reflecting the tool's purpose: sketching the perfect resume for each role.