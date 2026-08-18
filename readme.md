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

![Swagger UI](swagger.png)

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
