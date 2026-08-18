from fastapi import FastAPI, HTTPException

app = FastAPI()

# Your in-memory task list (placed at the top so it can be shared)
tasks = [
    {"id": 1, "title": "read book", "done": False},
    {"id": 2, "title": "play game", "done": True},
    {"id": 3, "title": "sleep", "done": False}
]

@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def status():
    return {"status": "ok"}

# 1. List all tasks (Required for Stage 2)
@app.get("/tasks")
def get_all_tasks():
    return tasks

# 2. Get a single task by ID with 404 error handling (Required for Stage 2)
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
    return task