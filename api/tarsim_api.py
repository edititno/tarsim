# Tarsim API v0.3
# AI Resume Tailoring Tool

import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from openai import OpenAI
import io

app = FastAPI(title='Tarsim API', version='0.3')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# OpenAI setup
OPENAI_KEY = os.environ.get('OPENAI_KEY', '')
openai_client = OpenAI(api_key=OPENAI_KEY)


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    text = ''
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text.strip()


def analyze_resume(resume_text: str) -> dict:
    """Send resume text to OpenAI for analysis."""
    prompt = f"""Analyze this resume and provide constructive improvement suggestions.

Resume text:
{resume_text}

Provide your response in this exact format:
1. STRENGTHS (3 specific strengths)
2. WEAKNESSES (3 specific weaknesses)
3. ATS_OPTIMIZATION (3 specific ATS keyword/formatting suggestions)
4. ACTION_VERB_UPGRADES (3 weak verbs to replace with stronger ones, format: "weak -> strong")
5. OVERALL_SCORE (out of 10)

Be specific. Reference exact text from the resume."""

    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=800,
        temperature=0.7
    )

    return {
        'analysis': response.choices[0].message.content,
        'tokens_used': response.usage.total_tokens
    }


def tailor_resume(resume_text: str, job_description: str) -> dict:
    """Tailor resume to a specific job description and generate a cover letter."""
    prompt = f"""You are an expert resume writer. Tailor the candidate's resume to match this specific job description, and write a custom cover letter.

CANDIDATE'S RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your response in this exact format:

===TAILORED_RESUME===
(Rewrite the resume to emphasize skills/experience matching this job. Keep all factual content true to the original — don't invent experience. Reorder bullets, rephrase descriptions, and integrate relevant keywords from the job description naturally. Output the full tailored resume as plain text.)

===COVER_LETTER===
(Write a 3-paragraph cover letter for this specific role. Tone: confident, professional, not generic. Reference specific points from the job description. Show genuine fit, not desperation.)

===KEY_CHANGES===
(Bullet point list of the main changes you made and why.)

===MATCH_SCORE===
(Score out of 10 for how well the candidate fits this role based on their existing experience.)

Be specific. Don't fabricate. Make it sound human, not robotic."""

    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=2000,
        temperature=0.7
    )

    return {
        'output': response.choices[0].message.content,
        'tokens_used': response.usage.total_tokens
    }


@app.get('/')
def home():
    return {
        'name': 'Tarsim API',
        'version': '0.3',
        'description': 'AI Resume Tailoring Tool',
        'status': 'running',
        'endpoints': ['/', '/analyze-resume', '/tailor-resume']
    }


@app.post('/analyze-resume')
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    """Upload a PDF resume and get improvement suggestions."""

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='File must be a PDF')

    try:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)

        if not resume_text:
            raise HTTPException(status_code=400, detail='No text found in PDF')

        result = analyze_resume(resume_text)

        return {
            'filename': file.filename,
            'text_length': len(resume_text),
            'analysis': result['analysis'],
            'tokens_used': result['tokens_used']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/tailor-resume')
async def tailor_resume_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Upload a PDF resume + job description, get tailored resume and cover letter."""

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='File must be a PDF')

    if len(job_description.strip()) < 50:
        raise HTTPException(status_code=400, detail='Job description too short (min 50 chars)')

    try:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)

        if not resume_text:
            raise HTTPException(status_code=400, detail='No text found in PDF')

        result = tailor_resume(resume_text, job_description)

        return {
            'filename': file.filename,
            'resume_length': len(resume_text),
            'job_description_length': len(job_description),
            'output': result['output'],
            'tokens_used': result['tokens_used']
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    print('=== Tarsim API v0.3 ===')
    print('Starting server on http://localhost:8000')
    uvicorn.run(app, host='0.0.0.0', port=8000)