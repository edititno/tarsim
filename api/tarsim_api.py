# Tarsim API v0.1
# AI Resume Tailoring Tool

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Tarsim API', version='0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def home():
    return {
        'name': 'Tarsim API',
        'version': '0.1',
        'description': 'AI Resume Tailoring Tool',
        'status': 'running'
    }


if __name__ == '__main__':
    import uvicorn
    print('=== Tarsim API v0.1 ===')
    print('Starting server on http://localhost:8000')
    uvicorn.run(app, host='0.0.0.0', port=8000)