# Pictures Service - Flask Application Reference

This directory contains the source code for the **Pictures microservice**, built using **Flask (Python)**.

This service is responsible for providing image data to the main Capstone application via a REST API. The data is loaded from the local file `backend/data/pictures.json`.

## I. Service Details

### 1. Technology and Endpoints

* **Framework:** Flask (Python)
* **Data Source:** Static JSON file (`pictures.json`)
* **Internal Base Endpoint:** `http://pictures:3000/picture` (for GET, POST)
* **Health Check:** `http://pictures:3000/health`
* **Count Check:** `http://pictures:3000/count`

### 2. Development Commands

These commands assume your entire Docker Compose environment is already running (via `docker compose up -d` executed from the project root directory).

#### Access the Container Shell

To execute Python commands or debug directly within the Pictures container:

```bash
docker compose exec pictures bash
```

#### Afficher les journaux de l'application

Pour diffuser en continu la sortie (journaux) du serveur Flask :

```bash
docker compose logs -f pictures
```

## II. Code Structure

* **`app.py`**: The main entry point for the Flask application.
* **`backend/routes.py`**: Defines all API routes (`/picture`, `/health`, `/count`) and the CRUD logic.
* **`backend/data/pictures.json`**: The static data source for the images.
* **`Dockerfile`**: Defines the container environment and dependencies.