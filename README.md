# SearchApp

## General Documentation and Installation Manual

### Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)


### Introduction
SearchApp is a powerful and efficient search application designed to help users quickly find information within large datasets.

### Features
- Fast and accurate search results


### Installation

#### Prerequisites
- Docker
- Docker Compose

#### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/fssappdev/search.git
    ```
2. Navigate to the project directory:
    ```bash
    cd searchapp
    ```
3. Set the database variables in the `.env` file:
    ```env
    POSTGRES_USER=your_database_user
    POSTGRES_PASSWORD=your_database_password
    POSTGRES_DB=your_database_name
    ```
4. Build and start the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```markdown
    ```

    ### Additional Information
    This command will:
    - Build the application container from the Dockerfile located in `./spsearch`.
    - Set up the PostgreSQL database with the `pgvector` extension.
    - Expose the application on port `8001` and PostgreSQL on port `5436`.
    ```
    ```

### Usage
To start the application, run:
```bash
python main.py
```

Once the containers are up and running, you can access the FastAPI application in your browser or API client: [http://localhost:8001](http://localhost:8001)

FastAPI documentation (with Swagger UI) will be available at: [http://localhost:8001/docs](http://localhost:8001/docs)


### Note
The application generates the embedding vector for the `vector_representation` column upon startup, so please leave that column blank.