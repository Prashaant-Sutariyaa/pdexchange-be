# FastAPI Backend Application

A scalable and production-ready backend REST API built using FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication, and Pydantic Settings.

---

## Features

- FastAPI framework
- PostgreSQL database integration
- SQLAlchemy ORM support
- JWT Authentication & Authorization
- Environment-based configuration using Pydantic Settings
- Password hashing with bcrypt
- Email configuration support
- Pydantic validation
- Auto-generated API documentation
- Modular and scalable architecture

---

## Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic v2
- JWT Authentication
- Uvicorn
- bcrypt
- python-jose

---

## Project Structure

```bash
project/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── routers/
│   │   └── auth.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── user.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   ├── utils/
│   │   └── hashing.py
│   │
│   └── main.py
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
```

```bash
cd your-repository-name
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
# Application
APP_NAME=SaaSApp
ENVIRONMENT=development

# JWT Configuration
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/your_database_name

# Mail Configuration
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

---

# Configuration

This project uses `pydantic-settings` for environment-based configuration management.

Example:

```python
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SaaSApp"
    ENVIRONMENT: str = "development"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str

    # Mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    class Config:
        env_file = (
            Path(__file__).resolve().parent.parent.parent / ".env"
        )


settings = Settings()
```

---

# Run Application

## Development Server

### Windows PowerShell

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI provides automatic interactive API documentation.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# Authentication

This project uses JWT token-based authentication.

## Authorization Header

```http
Authorization: Bearer your_access_token
```

---

# Database

This project uses PostgreSQL with SQLAlchemy ORM.

## Install PostgreSQL

Download PostgreSQL from:

```bash
https://www.postgresql.org/download/
```

---

# Main Dependencies

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose
passlib
bcrypt
pydantic
pydantic-settings
python-dotenv
```

---

# Generate Requirements File

```bash
pip freeze > requirements.txt
```

---

# Production Deployment

Recommended deployment platforms:

- Render
- Railway
- AWS
- Docker
- DigitalOcean

---

# License

This project is licensed under the MIT License.

---

# Author

Developed with ❤️ using FastAPI.
