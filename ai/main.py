from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="A simple in-memory REST API for managing tasks."
)


# -----------------------------
# Pydantic Models
# -----------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str = Field(...)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title must not be empty or whitespace.")

        return value


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title must not be empty or whitespace.")

        return value


# -----------------------------
# In-memory task storage
# -----------------------------

tasks: list[Task] = [
    Task(id=1, title="read book", done=False),
    Task(id=2, title="gaming", done=True),
    Task(id=3, title="scrolling", done=False),
]


# -----------------------------
# Helper function
# -----------------------------

def get_task_or_404(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found."
    )


# -----------------------------
# GET /
# -----------------------------

@app.get("/")
def root():
    return {
        "name": "Task Management API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /tasks": "Get all tasks",
            "GET /tasks/{task_id}": "Get a task by ID",
            "POST /tasks": "Create a new task",
            "PUT /tasks/{task_id}": "Update a task",
            "DELETE /tasks/{task_id}": "Delete a task"
        }
    }


# -----------------------------
# GET /health
# -----------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# -----------------------------
# GET /tasks
# -----------------------------

@app.get("/tasks")
def get_tasks():
    return tasks


# -----------------------------
# GET /tasks/{task_id}
# -----------------------------

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return get_task_or_404(task_id)


# -----------------------------
# POST /tasks
# -----------------------------

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must not be empty or whitespace."
        )

    # Generate the next available ID
    next_id = max((task.id for task in tasks), default=0) + 1

    new_task = Task(
        id=next_id,
        title=task_data.title,
        done=False
    )

    tasks.append(new_task)

    return new_task


# -----------------------------
# PUT /tasks/{task_id}
# -----------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate):
    task = get_task_or_404(task_id)

    # Check whether the request body is empty
    if not task_data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update data cannot be empty."
        )

    # Update only the fields that were provided
    if "title" in task_data.model_fields_set:
        if task_data.title is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be null."
            )

        task.title = task_data.title

    if "done" in task_data.model_fields_set:
        if task_data.done is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Done must be a boolean."
            )

        task.done = task_data.done

    return task


# -----------------------------
# DELETE /tasks/{task_id}
# -----------------------------

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):
    task = get_task_or_404(task_id)

    tasks.remove(task)

    return None