# Django Modular Project

A modular Django application that supports dynamic installation, upgrade, and removal of modules with role-based access control. This project is designed to demonstrate scalable Django architecture and best practices.

## 🔧 Features

- Modular architecture with install/upgrade/uninstall system
- Dynamic landing page generation per module
- Role-based access control:
  - **Admin**: Full CRUD access and module management
  - **Manager**: Limited CRUD and module management
  - **User**: CRU access
  - **Public**: Read-only access
- Uses:
  - Class-Based Views (CBV)
  - Middleware
  - `post_migrate` Signal
  - Mixins
  - Context Processor (for showing installed modules)
  - Tailwind CSS for styling
  - Custom Django Admin templates

## 🚀 Live Demo

Production URL:  
https://django-modular-project-production.up.railway.app

### Credentials

| Role    | Username | Password     |
|---------|----------|--------------|
| Admin   | admin    | admin123     |
| Manager | manager  | manager123   |
| User    | user     | user123      |
| Public  | public   | public123    |

## 💻 Running Locally

### Requirements

- Python 3.x
- pip
- virtualenv (optional but recommended)

### Setup

```bash
git clone https://github.com/eqqi33/django-modular-project.git
cd django-modular-project
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Open your browser at http://127.0.0.1:8000

## 🐳 Run with Docker

```bash
docker-compose up --build
```

Access via http://localhost:8000

## 📂 Project Structure

```
.
├── apps/
│   ├── engine_module/
│   └── example_module/
├── core/
│   └── context_processors.py
├── templates/
│   └── admin/  # Custom admin templates
├── static/
├── docker/
├── manage.py
└── requirements.txt
```

---

## 📄 License

This project is licensed for testing and demonstration purposes.
