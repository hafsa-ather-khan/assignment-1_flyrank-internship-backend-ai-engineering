# FastAPI Task API

A simple RESTful Task API built with **FastAPI** and **Pydantic**.

This project implements a complete CRUD API for managing tasks using an in-memory task list.

## Features

* Create tasks
* Get all tasks
* Get a single task by ID
* Update a task's title and/or completion status
* Delete tasks
* Request validation with Pydantic
* Proper HTTP status codes
* Interactive Swagger API documentation

## Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **Uvicorn**

## Installation & Running

Clone the repository and navigate into the project directory.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install fastapi uvicorn
```

Run the API:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Description         | Success Status |
| ------ | ------------------ | ------------------- | -------------- |
| GET    | `/`                | Get API information | 200            |
| GET    | `/health`          | Check API health    | 200            |
| GET    | `/tasks`           | Get all tasks       | 200            |
| GET    | `/tasks/{task_id}` | Get a task by ID    | 200            |
| POST   | `/tasks`           | Create a new task   | 201            |
| PUT    | `/tasks/{task_id}` | Update a task       | 200            |
| DELETE | `/tasks/{task_id}` | Delete a task       | 204            |

## Example: Create a Task

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Learn FastAPI\"}"
```

Example response:

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Learn FastAPI","done":false}
```

## Example: Get All Tasks

```bash
curl -i http://127.0.0.1:8000/tasks
```

## Example: Update a Task

```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/4 -H "Content-Type: application/json" -d "{\"title\":\"Master FastAPI\",\"done\":true}"
```

## Example: Delete a Task

```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/4
```

The API returns:

```text
HTTP/1.1 204 No Content
```

## Error Handling

The API returns appropriate status codes for invalid requests and unknown task IDs.

| Status | Meaning                                                  |
| -----: | -------------------------------------------------------- |
|    200 | Request successful                                       |
|    201 | Task successfully created                                |
|    204 | Task successfully deleted; no response body              |
|    400 | Invalid or empty request data                            |
|    404 | Task ID not found                                        |
|    422 | Request body does not match the expected Pydantic schema |

## Swagger UI

FastAPI automatically provides interactive API documentation through Swagger UI.


<img width="1366" height="677" alt="637727294-40a8d907-4d16-4ecd-bccc-ce17e2dfedbd" src="https://github.com/user-attachments/assets/b88f40a6-f4d1-4245-8963-fed52dbb7356" />


## Project Structure

```text
fastapi-task-api/
├── main.py
├── README.md
├── swagger.png
└── .gitignore
```

## Storage

Tasks are currently stored in an **in-memory Python list**.

This means all tasks are reset when the application restarts. No external database is required for this project.

## Project Status

🎉 Complete CRUD API implemented and published as part of the FastAPI internship assignments.


## AI vs Me

### My Prompt

I asked an AI assistant to build the same FastAPI Task API that I had already implemented by hand. The prompt specified Python, FastAPI, Pydantic, in-memory storage, the CRUD endpoints, validation rules, HTTP status codes, and Swagger UI.

The full prompt used for the AI version was:

> Build a complete REST API for a simple Task Management application using Python and FastAPI.
>
> Requirements:
>
> 1. Use FastAPI and Pydantic.
> 2. Store all tasks in an in-memory Python list. Do not use a database, files, or any external storage.
> 3. Start with these three example tasks:
>
>    * id: 1, title: "read book", done: false
>    * id: 2, title: "gaming", done: true
>    * id: 3, title: "scrolling", done: false
>
> Implement GET, POST, PUT, and DELETE endpoints for tasks, including appropriate validation, 200/201/204/400/404 status codes, and Swagger documentation at `/docs`.
>
> POST should require a non-empty title and trim whitespace. PUT should allow updating the title, done status, or both, and should reject an empty request body or invalid title. DELETE should return 204 with an empty body when successful.
>
> Keep the implementation beginner-friendly, use a single `main.py` file, and do not add a database or unnecessary dependencies.

### What the AI Did Better

**1. Centralized validation**

The AI used Pydantic's `field_validator` to validate and trim titles inside the Pydantic models. My implementation performed most of the validation inside the route functions.

This makes the AI version's validation logic more centralized and reusable.

**2. Reusable task lookup**

The AI created a `get_task_or_404()` helper function. This avoids repeating the same task lookup and 404 handling logic in multiple endpoints.

My implementation performed the lookup separately inside the individual route handlers.

**3. Stronger task typing**

My implementation stores tasks as dictionaries, while the AI created a Pydantic `Task` model with explicit types for `id`, `title`, and `done`.

This makes the structure of a task clearer and provides stronger type validation.

**4. Safer ID generation**

My implementation generates the next ID using the last task in the list. The AI uses the maximum existing ID plus one:

```python
max((task.id for task in tasks), default=0) + 1
```

This is safer if the task list is not ordered by ID.

### What the AI Got Wrong or Differently

The AI version did not exactly follow my error response structure.

My implementation returns errors using an `error` field inside the JSON detail, for example:

```json
{
  "detail": {
    "error": "Task 5 not found"
  }
}
```

The AI instead uses a plain FastAPI `detail` string:

```json
{
  "detail": "Task not found."
}
```

The HTTP status code is correct, but the response structure is different from my implementation.

### What My Prompt Forgot to Specify

My prompt described the required error responses as JSON error messages, but I did not explicitly specify the exact JSON structure.

I should have stated that error responses must contain an `error` field, for example:

```json
{
  "error": "Task not found"
}
```

Because I did not specify the exact structure, the AI made its own decision to use FastAPI's standard `detail` format.

### Rematch

For the second attempt, I would make the prompt more precise by explicitly defining the required JSON error response structure and requiring it consistently for all `400` and `404` responses.

The main lesson from the rematch was that a more precise prompt reduces the number of implementation decisions left for the AI.

