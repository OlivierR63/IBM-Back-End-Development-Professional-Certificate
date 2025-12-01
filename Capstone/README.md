# Capstone Service - Django Application

This directory contains the source code for the main application, built using **Django (Python)**. This service acts as the frontend, handles user authentication, data persistence (via SQLite), and communicates with the external microservices (Pictures and Songs).

## I. Development Commands

These commands assume your Docker Compose environment is already running (via `docker compose up -d` executed from the project root).

### 1. Access the Container Shell

To execute specific Django or Python commands directly within the Capstone container:

```bash
docker compose exec capstone bash
```

### 2. Database Maintenance

Use these commands when developing new features or modifying data models (execute these commands **while inside the container shell** or prefixed with `docker compose exec capstone`):

| Command | Purpose |
| :--- | :--- |
| `python manage.py makemigrations` | Creates new migration files based on changes to models (`models.py`). |
| `python manage.py migrate` | Applies existing migrations to the SQLite database. |
| `python manage.py createsuperuser` | Creates an administrative user for the Django admin panel. |
| `python manage.py runserver` | **Warning:** Runs the server locally inside the container (useful for debugging, though the main application is already exposed). |


### 3. Other Django Commands

Execute tests or check configurations:

```bash
python manage.py check
python manage.py test
```

---

## II. Application Access

Access the running application by the port forwarded by Docker Compose:

* **Main Application:** `http://localhost:8000/`
* **Admin Panel:** `http://localhost:8000/admin/`