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
- Object-level permission-based access control
- Dynamically calculated board statistics
- Django admin interface

## Tech Stack

- Python
- Django
- Django REST Framework
- Django REST Framework Token Authentication
- python-dotenv
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
│   ├── models.py
│   └── migrations/
│
├── board_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── admin.py
│   ├── models.py
│   └── migrations/
│
├── task_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── admin.py
│   ├── models.py
│   └── migrations/
│
├── .env.template
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

The local `.env` file, virtual environment, and SQLite database are not part of the repository.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/TemirlanGashimov/KinMindBackend.git
cd KinMindBackend
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file based on the provided `.env.template`.

#### Windows

```bash
copy .env.template .env
```

#### macOS / Linux

```bash
cp .env.template .env
```

Open the newly created `.env` file and replace the placeholder with your own Django secret key:

```env
SECRET_KEY=your-secret-key-here
```

The `.env` file contains sensitive configuration and must not be committed to version control.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

This step is optional but recommended if you want to use the Django admin interface.

```bash
python manage.py createsuperuser
```

### 7. Start the development server

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

The admin interface provides management views for:

- Users and user profiles
- Authentication tokens
- Boards
- Tasks
- Comments

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

The board list only contains boards where the authenticated user is the owner or a member.

Board details can only be accessed by the board owner or board members.

If a board exists but the authenticated user does not have access to it, the API returns `403 Forbidden`.

If the requested board does not exist, the API returns `404 Not Found`.

Board deletion is restricted to the board owner.

### Board Summary

Board list and board creation responses include dynamically calculated summary information.

Example response:

```json
{
  "id": 9,
  "title": "Board POST Test",
  "member_count": 2,
  "ticket_count": 0,
  "tasks_to_do_count": 0,
  "tasks_high_prio_count": 0,
  "owner_id": 3
}
```

The summary fields are:

- `member_count` - Number of members assigned to the board
- `ticket_count` - Total number of tasks belonging to the board
- `tasks_to_do_count` - Number of tasks with the `todo` status
- `tasks_high_prio_count` - Number of tasks with `high` priority
- `owner_id` - ID of the board owner

The board statistics are calculated dynamically from the current board members and tasks.

### Board Details

A successful `GET /api/boards/<board_id>/` request returns detailed board information including members and tasks.

The response can include:

- `id`
- `title`
- `owner_id`
- `members`
- `tasks`

Member information includes the user's ID, email address, and full name.

Task information includes task details such as title, description, status, priority, assignee, reviewer, due date, and comment count.

### Board Update

Board updates are performed using:

```text
PATCH /api/boards/<board_id>/
```

The request can contain fields such as:

```json
{
  "title": "Changed title",
  "members": [3, 4]
}
```

A successful update returns the updated board together with detailed owner and member information.

Example response:

```json
{
  "id": 9,
  "title": "Changed title",
  "owner_data": {
    "id": 3,
    "email": "max.mustermann@example.com",
    "fullname": "Max Mustermann"
  },
  "members_data": [
    {
      "id": 3,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    {
      "id": 4,
      "email": "test.user@example.com",
      "fullname": "Test User"
    }
  ]
}
```

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<task_id>/` | Retrieve task details |
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
- Board lists only include boards owned by the user or boards where the user is a member.
- Board details can only be accessed by the board owner or board members.
- Accessing an existing board without permission returns `403 Forbidden`.
- Requesting a board that does not exist returns `404 Not Found`.
- Only the board owner can delete a board.
- Tasks can only be created in accessible boards.
- Only the task creator or board owner can delete a task.
- Board members and owners can access task comments.
- Only the comment author can delete a comment.

## Environment Variables

The project uses environment variables for sensitive configuration.

The `.env.template` file documents the required variables:

```env
SECRET_KEY=your-secret-key-here
```

Create your own `.env` file for local development.

Never commit real secret keys or other sensitive credentials to the repository.

## Testing

Run the Django test suite with:

```bash
python manage.py test
```

The API should also be tested for:

- Successful requests
- Authentication errors
- Permission errors
- Validation errors
- Missing resources
- Correct HTTP status codes
- Correct response structures

Common status codes include:

| Status | Meaning |
|---|---|
| `200 OK` | Successful request |
| `201 Created` | Resource successfully created |
| `204 No Content` | Resource successfully deleted |
| `400 Bad Request` | Invalid request data |
| `401 Unauthorized` | Authentication credentials are missing or invalid |
| `403 Forbidden` | Resource exists, but the user does not have permission |
| `404 Not Found` | Requested resource does not exist |

## Code Quality

The project follows Django and Django REST Framework project conventions:

- Code structured according to PEP 8 conventions
- Explicit serializer fields instead of `__all__`
- Separate API modules for serializers, views, URLs, and permissions
- Dynamic querysets using `get_queryset()`
- Explicit permission classes
- Object-level permissions for protected resources
- Separate serializers for request validation and API response representation where required
- Resource-oriented API URLs
- No debug `print()` statements
- Clear separation between models, serializers, views, and permissions

## Development Checks

Before submitting or deploying the project, run:

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

`python manage.py makemigrations --check` should report:

```text
No changes detected
```

## Before Submission

Make sure that:

- `requirements.txt` is complete and up to date
- `README.md` is up to date
- `.env.template` is included
- `.env` is not committed
- `db.sqlite3` is not committed
- `.venv` is not committed
- No real secret keys are committed
- Database migrations are committed
- All required endpoints work as documented
- Success responses match the required API response structures
- Permission errors return the expected HTTP status codes

## Git Ignore

Local development files and sensitive configuration should not be committed.

Important ignored files and directories include:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
db.sqlite3
.vscode/
.idea/
```

The `.env.template` file is intentionally committed because it contains only placeholder values and documents the required environment variables.

## License

This project was developed as part of the KanMind backend project.