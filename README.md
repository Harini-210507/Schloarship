# Scholarship Application System

A complete full-stack web application for managing scholarship applications, document uploads, and administrator review — built with **Python Django**.

---

## Project Overview

Students can browse scholarships, submit applications, and upload required documents. Administrators can review each document individually, mark them as Verified or Rejected, and then approve or reject the overall application with a clear reason.

---

## Technology Stack

| Layer       | Technology                               |
|-------------|------------------------------------------|
| Backend     | Python 3.x, Django 6.x                   |
| Frontend    | Django Templates, HTML5, CSS3, Vanilla JS |
| Database    | SQLite (Django ORM)                      |
| File Upload | Django FileField + MEDIA_ROOT            |
| Auth        | Django built-in authentication           |

---

## Project Structure

```
scholarship_system/
├── manage.py
├── setup_demo.py            # Creates demo accounts and sample data
├── requirements.txt
├── README.md
├── .env.example
│
├── scholarship_system/      # Django project config
│   ├── settings.py
│   └── urls.py
│
├── accounts/                # User auth & student profiles
│   ├── models.py            # StudentProfile
│   ├── views.py             # register, login, logout, dashboard, profile
│   ├── forms.py
│   ├── urls.py
│   └── dashboard_urls.py
│
├── scholarships/            # Scholarship listings
│   ├── models.py            # Scholarship, RequiredDocument
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── applications/            # Application & document workflow
│   ├── models.py            # ScholarshipApplication, UploadedDocument
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── administrator/           # Admin review area
│   ├── views.py
│   └── urls.py
│
├── templates/               # All HTML templates
│   ├── base.html
│   ├── home.html
│   ├── 403.html / 404.html
│   ├── accounts/
│   ├── scholarships/
│   ├── applications/
│   └── administrator/
│
├── static/
│   ├── css/main.css
│   └── js/main.js
│
└── media/                   # Uploaded files (git-ignored)
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply Migrations

```bash
python manage.py migrate
```

### 3. Create Demo Data (accounts + 3 sample scholarships)

```bash
python setup_demo.py
```

This creates:

| Role    | Username  | Password     |
|---------|-----------|--------------|
| Admin   | admin     | Admin@1234   |
| Student | student1  | Student@1234 |

> **Important:** These credentials are for local development only. Change them before any deployment.

### 4. Run the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## Key Pages

| URL                          | Description                          |
|------------------------------|--------------------------------------|
| `/`                          | Home page                            |
| `/accounts/register/`        | Student registration                 |
| `/accounts/login/`           | Login (students and admin)           |
| `/scholarships/`             | Browse scholarships                  |
| `/scholarships/<id>/`        | Scholarship details & apply button   |
| `/dashboard/`                | Student dashboard                    |
| `/dashboard/profile/`        | Edit profile                         |
| `/applications/apply/<id>/`  | Start an application                 |
| `/applications/<id>/upload/` | Upload required documents            |
| `/applications/<id>/status/` | View application status & feedback   |
| `/admin-panel/`              | Administrator dashboard              |
| `/admin-panel/applications/<id>/review/` | Review & decide on an application |
| `/admin-panel/scholarships/` | Manage scholarships                  |
| `/django-admin/`             | Django built-in admin                |

---

## Core Workflow

```
Student registers → Browses scholarships → Applies → Uploads documents
       ↓
Admin reviews each document (Pending / Verified / Rejected)
       ↓
  All mandatory docs verified?
       ↓ Yes                          ↓ No
Admin Approves/Rejects           Student sees rejection reason & replaces document
       ↓
Student sees final status on their dashboard
```

---

## Data Models

### `StudentProfile`
- OneToOne with Django `User`
- Fields: `phone`, `date_of_birth`, `address`

### `Scholarship`
- Fields: `title`, `description`, `eligibility`, `amount`, `deadline`, `is_active`
- Created by admin users

### `RequiredDocument`
- FK → `Scholarship`
- Fields: `name`, `description`, `is_mandatory`, `order`

### `ScholarshipApplication`
- FK → `User` (student), `Scholarship`
- Status: `submitted` → `under_review` → `approved` / `rejected`
- Fields: `review_notes`, `reviewed_by`, `reviewed_at`

### `UploadedDocument`
- FK → `ScholarshipApplication`, `RequiredDocument`
- Status: `pending` → `verified` / `rejected`
- Fields: `file`, `rejection_reason`, `reviewed_at`

---

## Security Features

- **CSRF protection** on all forms (Django built-in)
- **Role-based access** via `student_required` and `admin_required` decorators
- **Students** can only view and edit their own applications
- **File validation**: only PDF, JPG, JPEG, PNG; max 5 MB
- **Media files** served only in DEBUG mode; not publicly listed
- **Passwords** hashed by Django (PBKDF2 + SHA256)
- **No hard-coded credentials** — demo accounts created via setup script

---

## Django Concepts Demonstrated

1. **Custom User Profiles** — `OneToOneField` on `User`
2. **ModelForms** — with custom `clean_*` validation
3. **File Uploads** — `FileField`, `upload_to`, `MEDIA_ROOT/URL`
4. **Django Messages** — flash messages for user feedback
5. **Template Inheritance** — `{% extends %}` and `{% block %}`
6. **URL Namespacing** — `app_name` and `{% url 'ns:name' %}`
7. **ORM Queries** — `select_related`, `prefetch_related`, `filter`, `get_or_create`
8. **Role-based Decorators** — custom view wrappers
9. **Django Admin** — registered models with `list_display`, `search_fields`, inlines
10. **Django Authentication** — `login`, `logout`, `UserCreationForm`

---

## Creating Your Own Admin Account

```bash
python manage.py createsuperuser
```

---

## Notes

- Uploaded files are stored in `media/applications/<id>/` and are not directly accessible without knowing the URL.
- This project uses SQLite for simplicity. For production, switch to PostgreSQL and set `DEBUG=False`.
- Document uploads are validated for type and size but are not legally authenticated.

