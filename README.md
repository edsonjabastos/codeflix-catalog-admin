# Codeflix Project

## Overview

Codeflix is a project designed to manage categories and genres for a media catalog. It includes functionalities for creating, updating, listing, and deleting categories and genres. The project is structured to support both unit and integration tests, ensuring robust and reliable code.

## Features

- Create, update, list, and delete categories and genres.
- Integration with Django Rest Framework for API endpoints.
- Comprehensive test coverage using pytest.
- Docker support for containerized deployment.

## Project Structure

```
codeflix/
├── src/
│   ├── django_project/
│   │   ├── category_app/
│   │   ├── genre_app/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   ├── core/
│   │   ├── category/
│   │   ├── genre/
│   ├── manage.py
├── tests_e2e/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/edsonjabastos/codeflix.git
    cd codeflix
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Running the Project

1. Apply migrations:

    ```sh
    python src/manage.py migrate
    ```

2. Run the development server:

    ```sh
    python src/manage.py runserver
    ```

3. Access the application at `http://127.0.0.1:8000/`.

### Running Tests

To run the tests, use the following command:

```sh
pytest
```

### Using Docker

1. Build the Docker image:

    ```sh
    docker build -t codeflix-catalog-admin .
    ```

2. Run the Docker container:

    ```sh
    docker run -d -v ./src:/app codeflix-catalog-admin
    ```

## API Endpoints

### Categories

- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category
- `GET /api/categories/{id}/` - Retrieve a category by ID
- `PUT /api/categories/{id}/` - Update a category by ID
- `PATCH /api/categories/{id}/` - Partially update a category by ID
- `DELETE /api/categories/{id}/` - Delete a category by ID

### Genres

- `GET /api/genres/` - List all genres
- `POST /api/genres/` - Create a new genre
- `GET /api/genres/{id}/` - Retrieve a genre by ID
- `PUT /api/genres/{id}/` - Update a genre by ID
- `DELETE /api/genres/{id}/` - Delete a genre by ID

