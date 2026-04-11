from .server import app
from .client.rq_client import celery_app
from dotenv import load_dotenv
import uvicorn
import sys

load_dotenv()

def main():
    # Run FastAPI server
    uvicorn.run(app, port=8000, host="localhost")

def run_worker():
    # Run Celery worker
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '-P', 'solo'  # Use solo pool for better Windows compatibility
    ])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'worker':
        run_worker()
    else:
        main()