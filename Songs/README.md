# Songs Service - Flask API with MongoDB

This directory contains the source code for the **Songs microservice**, built using **Flask (Python)**.

This service implements a full **RESTful API** for managing song data, with persistent storage provided by the **MongoDB** database. It is designed to run within the Docker Compose environment.

## I. Service Details

### 1. Technology and Endpoints

* **Framework:** Flask (Python)
* **Database:** MongoDB
* **Internal Endpoint:** `http://songs:8000/song`
* **Internal Port:** 8000

### 2. Development Commands

These commands are executed inside the container and assume your entire Docker Compose environment is running (via `docker compose up -d` executed from the project root).

#### Access the Container Shell

To execute Python commands or debug directly within the Songs container:

```bash
docker compose exec songs bash
```

#### Afficher les journaux de l'application

Pour diffuser en continu la sortie (journaux) du serveur Flask :

```bash
docker compose logs -f songs
```

### Exécuter les tests
Pour lancer les tests automatisés avec Pytest (en supposant que les dépendances soient installées dans le conteneur) :

```bash
docker compose exec songs pytest
```

## II. API Endpoints Reference

The main application (Capstone) accesses these endpoints via the internal service name `songs:8000`.

| Method | Endpoint | Description |
| :----- | :------- | :---------- |
| `GET` | `/health` | Checks the health status of the API. |
| `GET` | `/count` | Gets the total number of songs in the database. |
| `GET` | `/song` | Retrieves all songs. |
| `GET` | `/song/{id_str}` | Retrieves a specific song by its numerical ID. |
| `POST` | `/song` | Creates a new song. |
| `PUT` | `/song/{id_str}` | Updates an existing song by its ID. |
| `DELETE` | `/song/{id_str}` | Deletes a song by its ID. |


## III. Code Structure

* **`app.py`**: The main entry point for the Flask application.
* **`backend/routes.py`**: Defines all API routes and the CRUD logic using PyMongo to interact with MongoDB.
* **`entrypoint.sh`**: Ensures MongoDB is available before launching the Flask server.
* **`Dockerfile`**: Defines the container environment and dependencies.