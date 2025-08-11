# Back-End Development Songs API

## Project Overview

This project is a RESTful API built with **Flask** for managing a collection of songs, with data stored in a **MongoDB** database. It provides endpoints for common operations such as retrieving all songs, getting a song by ID, adding new songs, updating existing ones, and deleting them.

## Features

* **RESTful Endpoints**: Standard CRUD operations (Create, Read, Update, Delete) for songs.
* **MongoDB Integration**: Persistent storage for song data.
* **ID-based Management**: Songs are managed using a unique numerical ID.
* **Error Handling**: Robust error responses for invalid requests (e.g., malformed IDs, non-existent resources).
* **Health Check**: An endpoint to monitor the API's operational status.
* **Unit/Integration Tests**: Comprehensive test suite using Pytest to ensure API reliability.

## Technologies Used

* **Python 3.x**
* **Flask**: Web framework for building the API.
* **PyMongo**: Python driver for MongoDB.
* **MongoDB**: NoSQL database for data storage.
* **Pytest**: Testing framework.
* **python-dotenv**: For managing environment variables. (If you use it for DB connection strings, etc.)
* **Gunicorn / Waitress**: (Mention if you plan to use a WSGI server for deployment)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
* **Python 3.8+**
* **pip** (Python package installer)
* **MongoDB Community Server** (running locally or accessible remotely)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/Back-End-Development-Songs.git](https://github.com/YourUsername/Back-End-Development-Songs.git)
    cd Back-End-Development-Songs
    ```

2.  **Create a virtual environment an install the dependancies:**
    ```bash 
    ./bin/setup.sh
    exit
    ```

3.  **Start the MongoDB server:**
    Retrieve the user name, the mongoDB hostname and the password

### Running the Application

1.  **Open a new terminal window, configure 3 Environment Variables and run the Flask application:**
    ```bash 
    cd Back-End-Development-Songs
    export MONGODB_USERNAME = 'root'
    export MONGODB_PASSWORD = password
    export MONGODB_SERVICE = MongoDB hostname ( It looks like an IP adress)
    flask run --reload --debugger
    ```

2.  **Keep this terminal as is and open a second terminal**
    ```bash
    cd Back-End-Development-Songs
    export MONGODB_USERNAME = 'root'
    export MONGODB_PASSWORD = password
    export MONGODB_SERVICE = MongoDB hostname ( It looks like an IP adress)
    ```
    In order to test the /health endpoint, launch the command below:
    ```bash
    curl -X GET -i -w '\n' localhost:5000/health
    ```

    For testing the /count endpoint : 
    ```bash
    curl -X GET -i -w '\n' localhost:5000/count
    ```
    And so on ...
    
## API Endpoints

Here's a summary of the available API endpoints:

| Method | Endpoint              | Description                                        | Request Body (JSON)                                    | Response (JSON)                                                                                                    |
| :----- | :-------------------- | :------------------------------------------------- | :----------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `GET`  | `/health`             | Checks the health status of the API.               | None                                                   | `{"status": "OK"}` (200)                                                                                           |
| `GET`  | `/count`              | Gets the total number of songs.                    | None                                                   | `{"count": <number_of_songs>}` (200)                                                                               |
| `GET`  | `/song`               | Retrieves all songs.                               | None                                                   | `{"songs": [...]}` (200)                                                                                           |
| `GET`  | `/song/{id_str}`      | Retrieves a specific song by its numerical ID.     | None                                                   | `{"id": ..., "title": ..., ...}` (200) or `{"message": "ERROR: song not found"}` (404)                             |
| `POST` | `/song`               | Creates a new song.                                | `{"id": <int>, "title": <str>, "artist": <str>, ...}`  | `{"inserted_id": "..."}` (201) or `{"message": "song with id X already present"}` (302) or `{"message": "ERROR: Invalid ID"}` (400) |
| `PUT`  | `/song/{id_str}`      | Updates an existing song by its ID.                | `{"title": <str>, "artist": <str>, ...}`               | `{"id": ..., "title": ..., ...}` (201) or `{"message": "Song not found"}` (404) or `{"message": "Song found, but nothing updated"}` (200) |
| `DELETE` | `/song/{id_str}`    | Deletes a song by its ID.                          | None                                                   | (204 No Content) or `{"message": "Song not found"}` (404) or `{"message": "ERROR: Invalid ID"}` (400)             |

*(Replace `{id_str}` with the actual song ID, e.g., `/song/1`)*

## Running Tests

To run the automated tests for the API:

1.  **Ensure your virtual environment is active.**
2.  **Navigate to the `Back-End-Development-Songs` directory:**
    ```bash
    cd Back-End-Development-Songs
    ```
3.  **Run Pytest:**
    ```bash
    pytest
    ```
    Or to run a specific test:
    ```bash
    pytest -k 'test_health'
    ```

## Contributing

(Optional section)
If you wish to contribute to this project, please follow these steps:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.
