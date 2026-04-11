from fastapi import FastAPI, Query
from celery.result import AsyncResult
from .queues.worker import process_query

app = FastAPI()

    
@app.get('/')
def root():
    return {"Status" : "Server is running..."}

@app.post('/chat')
def chat(
    query : str = Query(...,description="The chat query")
):
    task = process_query.delay(query)
    return {"Status" : "queued", "job_id": task.id}

@app.get('/job-status')
def get_result(
    job_id: str = Query(...,description="Job ID")
):
    task_result = AsyncResult(job_id, app=process_query.app)
    
    if task_result.status == 'PENDING':
        return {"status": "pending", "result": None}
    elif task_result.status == 'SUCCESS':
        return {"status": "success", "result": task_result.result}
    elif task_result.status == 'FAILURE':
        return {"status": "failure", "result": str(task_result.info)}
    else:
        return {"status": task_result.status, "result": None}