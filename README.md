# TeamBoard Backend

Django REST Framework backend for the TeamBoard B2B Knowledge Base API.

## Tech Stack
- Python 3.12+
- Django 6.1.1
- Django REST Framework 3.18.1
- djangorestframework-simplejwt 5.5.1
- PostgreSQL 17
- Docker / Docker Compose
- python-dotenv

## Setup

### 1. Install dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Environment variables

Create `.env` in the project root:

```env
SECRET_KEY=replace-with-a-secure-secret
POSTGRES_DB=teamboard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5434
```

Do not commit `.env`.

### 3. Start PostgreSQL

```powershell
docker compose up -d
```

The supplied compose file maps host port `5434` to PostgreSQL container port `5432`.

### 4. Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Run server

```powershell
python manage.py runserver
```

Base URL:

`http://127.0.0.1:8000`

## Authentication

Registration and login are public. Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

A User `post_save` signal automatically creates the related Company and generates its API key using `secrets.token_urlsafe(32)`.

## Required API Endpoints

### Register

`POST /api/auth/register/`

```json
{
  "username": "acmecorp",
  "password": "securepass123",
  "company_name": "Acme Corp",
  "email": "dev@acmecorp.com"
}
```

Returns username, company name, generated API key and JWT access token.

### Login

`POST /api/auth/login/`

```json
{
  "username": "acmecorp",
  "password": "securepass123"
}
```

Returns JWT access token, company name and API key.

### Knowledge Base Query

`POST /api/kb/query/`

Requires JWT.

```json
{
  "search": "select_related"
}
```

Searches both `question` and `answer` using case-insensitive matching. Every query is logged, including zero-result queries. Search and logging occur inside `transaction.atomic()`.

### Admin Usage Summary

`GET /api/admin/usage-summary/`

Requires JWT and `Company.role == admin`.

Returns:
- total queries
- distinct active companies
- top 5 search terms

Client users receive HTTP 403.

## Seeding KB Entries

At least 10 KB entries should be present for testing. You can use the Django shell:

```powershell
python manage.py shell
```

Example:

```python
from api.models import KBEntry

KBEntry.objects.create(
    question="What is select_related in Django ORM?",
    answer="select_related performs a SQL JOIN and fetches related objects in the same query.",
    category="database",
)

KBEntry.objects.create(
    question="What is transaction.atomic()?",
    answer="transaction.atomic() groups database operations into a transaction.",
    category="database",
)

KBEntry.objects.create(
    question="What is a JWT token?",
    answer="JWT is a signed token commonly used for stateless authentication.",
    category="api",
)

KBEntry.objects.create(
    question="When should I use Q objects?",
    answer="Q objects allow complex database queries using AND, OR and NOT conditions.",
    category="database",
)
```

Add additional entries so searches can return multiple results.

## Validation

Run:

```powershell
python manage.py check
```

## Postman

Import `TeamBoard_Postman_Collection.json`.

The collection contains 11 scenarios:
1. Register success
2. Duplicate registration
3. Login success
4. Invalid login
5. Authenticated KB query
6. KB query without token
7. Blank KB search
8. KB query with zero results
9. Admin usage without token
10. Admin usage with client token
11. Admin usage with admin token

The collection uses `{{base_url}}` with default value `http://127.0.0.1:8000`.

## Git

The `.gitignore` should exclude:

```text
.env
venv/
__pycache__/
*.pyc
```
