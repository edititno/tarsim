# Tarsim API v0.2
# AI Resume Tailoring Tool

import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from openai import OpenAI
import io

app = FastAPI(title='Tarsim API', version='0.2')

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


@app.get('/')
def home():
    return {
        'name': 'Tarsim API',
        'version': '0.2',
        'description': 'AI Resume Tailoring Tool',
        'status': 'running',
        'endpoints': ['/', '/analyze-resume']
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


if __name__ == '__main__':
    import uvicorn
    print('=== Tarsim API v0.2 ===')
    print('Starting server on http://localhost:8000')
    uvicorn.run(app, host='0.0.0.0', port=8000)