# IBM Back-End Development Professional Certificate

This repository consolidates three projects developed as part of the IBM Back-End Development Professional Certificate. Each project demonstrates different aspects of back-end development using various technologies and frameworks.

## Projects Overview

### Back-End Development Songs API

A RESTful API built with **Flask** for managing a collection of songs, with data stored in a **MongoDB** database. This project provides endpoints for common CRUD operations and includes features such as:

- **RESTful Endpoints**: Standard CRUD operations for songs.
- **MongoDB Integration**: Persistent storage for song data.
- **Error Handling**: Robust error responses for invalid requests.
- **Health Check**: Endpoint to monitor the API's operational status.
- **Unit/Integration Tests**: Comprehensive test suite using Pytest.

**Technologies Used**: Python 3.x, Flask, PyMongo, MongoDB, Pytest.

### Back-End Development Pictures

This project focuses on managing and displaying pictures. It integrates with a back-end service to retrieve and manage picture data.

### Back-End Development Capstone

A Django-based application showcasing the integration of various back-end components, including user authentication, database management, and REST API consumption. Key features include:

- **Django Framework**: Utilized for building the web application.
- **Database Migrations**: Handling schema changes and database setup.
- **Admin Interface**: Automatic admin interface for managing content.
- **Containerization**: Docker support for easy deployment and scaling.

**Technologies Used**: Python, Django, SQLite/MySQL, Docker.

## Getting Started

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **MongoDB Community Server** (for the Songs API)
- **Docker** (for containerization of the Capstone project)

### Installation and Running the Applications

#### Songs API

1. Clone the repository and navigate to the Songs directory.
2. Set up a virtual environment and install dependencies.
3. Configure environment variables for MongoDB and run the Flask application.

#### Capstone Project

1. Clone the repository and navigate to the Capstone directory.
2. Install the required packages using `pip install -r requirements.txt`.
3. Apply database migrations and run the Django server.
4. Access the application and admin interface via the provided URLs.

## API Endpoints and Features

- **Songs API**: Offers endpoints for managing songs, including health checks, song retrieval, creation, updates, and deletion.
- **Capstone Project**: Features user authentication, concert management, and integration with external APIs for dynamic content.

## Running Tests

Each project includes a suite of tests to ensure functionality and reliability. Navigate to the respective project directory and run the tests using `pytest` or Django's test runner.

## Contributing

Contributions to these projects are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Open a Pull Request to the main repository.

## License

This project is licensed under the terms of the MIT license.
