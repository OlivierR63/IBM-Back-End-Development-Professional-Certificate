
# IBM-Back-End-Development-Professional-Certificate

This repository contains the source code and configuration for the Capstone project, implementing a microservices architecture for a concert management application, orchestrated using **Docker Compose**.

## Architecture Overview

The application is composed of four main services that communicate over a dedicated Docker network:

| Service | Technology | Role | Internal URL (Endpoint Example) |
| :--- | :--- | :--- | :--- |
| **Capstone** | **Django (Python)** | Main application, frontend, user authentication, and data persistence (SQLite). | N/A (Main Service) |
| **Pictures** | **Flask (Python)** | Provides image data from a static JSON file. | `http://pictures:3000/picture` |
| **Songs** | **Flask (Python) / PyMongo** | Provides song metadata from a MongoDB database. | `http://songs:8000/song` |
| **MongoDB** | **MongoDB** | Persistent database for the Songs microservice. | `mongodb:27017` |

## Prerequisites

You must have the following installed and configured on your machine to run the project:

* **Docker**
* **Docker Compose** (or Docker v24+ which integrates it via `docker compose`)

---

## I. Quick Start: Launching the Application

**IMPORTANT :** All commands in this section must be executed from the repository's **root directory** (`IBM-Back-End-Development-Professional-Certificate/`).

### 1. Start the Architecture

#### Option A: Using the Windows Script (`start.bat`)

For Windows users, execute the `start.bat` script. This script automatically runs the full build and launch command in detached mode.

| Environment | Command |
| :--- | :--- |
| **Command Prompt / Git Bash** | `start.bat` |
| **PowerShell** | `.\start.bat`

#### Option B: Manual Command (Recommanded for all non-batch users)

This command builds the images, sets up the network, and starts all services in the background (`-d`).

```bash
docker compose up -d --build
```

### 2\. Initialize the Database and Fix Permissions

Before running the application, you must apply migrations and correct file permissions on the SQLite database used by Django.

| Command | Purpose |
| :--- | :--- |
| `docker compose exec capstone python manage.py migrate` | Applies Django migrations and creates the database schema. |
| `docker compose exec -u root capstone chown appuser:appuser /opt/app-root/src/db.sqlite3` | **CRITICAL:** Fixes the 'readonly database' error by giving ownership to the application user (`appuser`). |
| `docker compose exec capstone python manage.py createsuperuser` | Creates an admin user for the Django panel. |

### 3\. Access the Application

The services are mapped to specific ports on the host machine:

| Service | Host Port | Internal Port | URL d'accès |
| :--- | :--- | :--- | :--- |
| **Capstone (Main)** | `8000` | `8000` | `http://localhost:8000/` |
| **Songs API** | `8001` | `8000` | `http://localhost:8001/song` |
| **Pictures API** | `8002` | `3000` | `http://localhost:8002/picture` |
| **Admin Panel** | `8000` | `8000` | `http://localhost:8000/admin/` |

-----

## II. Development and Maintenance

### 1\. Check Service Status

View the status and health of all running containers:

```bash
docker compose ps
```

### 2\. Run Automated Tests

| Service | Framework | Command |
| :--- | :--- | :--- |
| **Capstone (Django)** | Django Test Runner | `docker compose exec capstone python manage.py test` |
| **Songs / Pictures** | Pytest | `docker compose exec [songs/pictures] pytest` |

*(Note: Pytest is configured via `pytest.ini` at the root of the project.)*

**Justification for Test Commands:**

* **Django** is an "all-in-one" framework that uses its own internal utility (`manage.py`) to execute tests (integrated method).
* **Flask** is a lightweight micro-framework that does not provide a native test runner. We therefore use the external tool **Pytest** (`pytest`) for the Songs and Pictures microservices.

### 3\. Debugging (Accessing Containers)

| Service | Command |
| :--- | :--- |
| **Capstone (Django)** | `docker compose exec capstone bash` |
| **Songs (Flask) ** |  `docker compose exec songs bash`|
| **Pictures (Flask)** |`docker compose exec pictures bash\` |

### 4\. Stop and Cleanup

| Command | Purpose |
| :--- | :--- |
| `docker compose stop` | Stops the running containers but preserves their state (and volumes). |
| `docker compose down` | Stops containers and removes containers and networks. |
| `docker compose down -v` | **Full Cleanup:** Stops containers, removes containers, networks, and all **volumes** (including MongoDB data).
