from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# In-memory task list
tasks = [
    {"id": 1, "title": "read book", "done": False},
    {"id": 2, "title": "play game", "done": True},
    {"id": 3, "title": "sleep", "done": False}
]

# Optional: Using Pydantic for request body structure validation
class TaskCreate(BaseModel):
    title: str

@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
    return task

# Stage 3: Create a new task with validation and 201 status code
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: dict):
    # Validate that 'title' exists and is not an empty string or just whitespace
    title = task_data.get("title")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail={"error": "Title is required and cannot be empty"})
    
    # Generate the next free ID automatically
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    
    # Create the new task object
    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }
    
    # Add it to our in-memory list
    tasks.append(new_task)
    
    return new_task