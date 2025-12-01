This repository contains the source code and configuration for the Capstone project, implementing a microservices architecture for a concert management application, orchestrated using **Docker Compose**.

## Architecture Overview

The application is composed of three main microservices that communicate over a dedicated Docker network:

| Service | Technology | Role | Internal URL (Endpoint Example) |
| :--- | :--- | :--- | :--- |
| **Capstone** | **Django (Python)** | Main application, frontend, user authentication, and data persistence (SQLite). | N/A (Main Service) |
| **Pictures** | **Flask (Python)** | Provides image data. | `http://pictures:3000/picture` |
| **Songs** | **Node.js (Express)** | Provides song metadata. | `http://songs:8000/song` |

## Prerequisites

You must have the following installed and configured on your machine to run the project:

* **Docker**
* **Docker Compose** (or Docker v24+ which integrates it via `docker compose`)

---

## I. Quick Start: Launching the Application

These commands are executed from this repository's root directory (`IBM-Back-End-Development-Professional-Certificate/`).

### 1. Start the Architecture

This command builds the images, sets up the network, and starts all services in the background (`-d`).

```bash
docker compose up -d --build
```

### 2. Initialize the Database and Fix Permissions

Before running the application, you must apply migrations and correct file permissions on the SQLite database used by Django.

| Command | Purpose |
| :--- | :--- |
| `docker compose exec capstone python manage.py migrate` | Applies Django migrations and creates the database schema. |
| `docker compose exec -u root capstone chown appuser:appuser /opt/app-root/src/db.sqlite3` | **CRITICAL:** Fixes the 'readonly database' error by giving ownership to the application user (`appuser`). |
| `docker compose exec capstone python manage.py createsuperuser` | Creates an admin user for the Django panel. |

### 3. Access the Application

The main application is exposed on port `8000`.

* **Main Application:** `http://localhost:8000/`
* **Admin Panel:** `http://localhost:8000/admin/` (Use the superuser created above)


---

## II. Development and Maintenance

### 1. Check Service Status

View the status and health of all running containers:

```bash
docker compose ps
```

### 2. Stop and Cleanup

| Command | Purpose |
| :--- | :--- |
| `docker compose stop` | Stops the running containers but preserves their state (and volumes). |
| `docker compose down` | Stops containers and removes containers and networks. |
| `docker compose down -v` | **Full Cleanup:** Stops containers, removes containers, networks, and all **volumes** (including MongoDB data). |

### 3. Debugging (Accessing the Capstone Container)

To run specific Django commands or debug inside the main application container:

```bash
docker compose exec capstone bash
```