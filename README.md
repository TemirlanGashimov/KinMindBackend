# KanMind Backend

KanMind is a REST API for a Kanban-style project management application.

The backend is built with Django and Django REST Framework and provides authentication, board management, task management, comments, user assignment, and permission-based access control.

## Features

- User registration and token-based authentication
- Create, update, list, and delete Kanban boards
- Add users as board members
- Search users by email
- Create and manage tasks
- Assign tasks to users
- Assign reviewers to tasks
- Task status and priority management
- Due dates
- Comments on tasks
- Permission-based access control
- Django admin interface

## Tech Stack

- Python
- Django
- Django REST Framework
- Token Authentication
- SQLite for local development

## Project Structure

```text
backend/
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── auth_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── admin.py
│   └── models.py
│
├── board_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── admin.py
│   └── models.py
│
├── task_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── admin.py
│   └── models.py
│
├── manage.py
└── requirements.txt
```

> The local SQLite database (`db.sqlite3`) must not be committed to the repository.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/TemirlanGashimov/KinMindBackend
cd KinMindBackend
```

Replace `<YOUR-REPOSITORY-URL>` with the URL of this repository.

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

This step is optional but recommended if you want to use the Django admin interface.

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The backend is then available at:

```text
http://127.0.0.1:8000/
```

The API endpoints are available below:

```text
http://127.0.0.1:8000/api/
```

## Django Admin

After creating a superuser, the Django admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

## Authentication

Protected endpoints require token authentication.

Send the authentication token in the request header:

```text
Authorization: Token <your-token>
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Login and receive an authentication token |

### Boards

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/boards/` | List boards accessible to the current user |
| POST | `/api/boards/` | Create a board |
| GET | `/api/boards/<board_id>/` | Retrieve board details |
| PATCH | `/api/boards/<board_id>/` | Update a board |
| DELETE | `/api/boards/<board_id>/` | Delete a board |
| GET | `/api/email-check/` | Find a user by email |

Board deletion is restricted to the board owner.

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/tasks/` | Create a task |
| PATCH | `/api/tasks/<task_id>/` | Update a task |
| DELETE | `/api/tasks/<task_id>/` | Delete a task |
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to the current user |
| GET | `/api/tasks/reviewing/` | List tasks where the current user is the reviewer |

Tasks can only be created inside boards that the authenticated user is allowed to access.

Task deletion is restricted to the task creator or the board owner.

### Comments

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/<task_id>/comments/` | List comments for a task |
| POST | `/api/tasks/<task_id>/comments/` | Create a comment |
| DELETE | `/api/tasks/<task_id>/comments/<comment_id>/` | Delete a comment |

Users must have access to the corresponding board to view or create task comments.

Only the author of a comment can delete that comment.

## Task Fields

Tasks support the following status values:

```text
todo
in_progress
review
done
```

Tasks support the following priority values:

```text
low
medium
high
```

Task responses can include:

- ID
- Board
- Title
- Description
- Status
- Priority
- Assignee
- Reviewer
- Due date
- Comment count

## Permissions

The API uses authentication and object-level permissions.

Important permission rules include:

- Only authenticated users can access protected endpoints.
- Users can access boards they own or belong to.
- Only the board owner can delete a board.
- Tasks can only be created in accessible boards.
- Only the task creator or board owner can delete a task.
- Board members and owners can access task comments.
- Only the comment author can delete a comment.

## Testing

Run the Django test suite with:

```bash
python manage.py test
```

Before submitting the project, the API should also be tested for:

- successful requests
- authentication errors
- permission errors
- validation errors
- missing resources
- correct HTTP status codes

Expected status codes include:

| Status | Meaning |
|---|---|
| `200 OK` | Successful request |
| `201 Created` | Resource successfully created |
| `204 No Content` | Resource successfully deleted |
| `400 Bad Request` | Invalid request data |
| `401 Unauthorized` | Authentication credentials missing or invalid |
| `403 Forbidden` | User does not have permission |
| `404 Not Found` | Resource does not exist |

## Code Quality

The project follows the defined Django/DRF project conventions:

- PEP 8 compliant Python code
- Explicit serializer fields instead of `__all__`
- Separate API folders for serializers, views, URLs, and permissions
- Dynamic querysets using `get_queryset()`
- Explicit permission classes
- Resource-oriented API URLs
- No debug `print()` statements
- No commented-out development code
- Clear separation between models, serializers, views, and permissions

## Before Submission

Before submitting the project, verify:

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

Also make sure that:

- `requirements.txt` is complete
- `README.md` is up to date
- `db.sqlite3` is not committed
- the virtual environment is not committed
- sensitive configuration is not committed
- all required endpoints work as documented

## Git Ignore

At minimum, the repository should ignore local development files such as:

```gitignore
venv/
.venv/
__pycache__/
*.pyc
db.sqlite3
.env
.vscode/
.idea/
```