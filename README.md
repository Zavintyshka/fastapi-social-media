# Social Media API

## 1. About

This API is built with the FastAPI framework in Python, using PostgreSQL as the database. Database migrations are managed with Alembic. The API includes the following features:

- User registration
- User authentication using JWT tokens
- Creating posts
- Like system

## 2. Installation - General

The application can be deployed in various ways:

- Run it on your local machine
- Deploy it on a virtual machine with Ubuntu
- Deploy it using Docker

Create a directory named `source` where the application logic `app` and other auxiliary files will reside. To clone the project, use the command `git clone https://github.com/Zavintyshka/fastapi-social-media path/to/app`. For proper operation, change the variable `TEST_MODE=False` in `app/settings.py`.

## 2.1 Environment Variables

You need to set environment variables for any deployment method.

### 2.1.1 General Env

The main `.env` file should be located in `path/to/app/`. It should contain the following fields:

- DB_USER
- DB_PASSWORD
- SECRET_KEY (can be generated using `openssl rand -hex 32`)
- HOST
- DB_NAME
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

### 2.1.2 Env for Docker

Docker also requires environment variables for the PostgreSQL container. The `postgres.env` file should be located in the `/path/to/source/envs_for_docker` directory. The structure of this file:

- POSTGRES_PASSWORD
- POSTGRES_DB

### 2.1.3 Env for Tests

To avoid losing data from the main database, a separate database is used for testing. The configuration for this database is stored in a `.env` file, which should be placed in `/path/to/source/app/tests`. It should contain the following variables:

- DB_USER_TEST
- DB_PASSWORD_TEST
- HOST_TEST
- DB_NAME_TEST

## 2.2 Setup on Local Machine

For this method, you will need to install PostgreSQL. Additionally, set up a virtual environment with all dependencies:

```bash
python3 -m venv path/to/source/venv # create venv
source ~/venv/bin/activate # activate the virtual environment
pip install -r path/to/requirements.txt # install the necessary libraries
```

To run the application, use the Uvicorn library:
`uvicorn path.to.app.folder.start_server:app`

To specify the address and ports, use the following flags:

- `--host 0.0.0.0`
- `--port 8000`

## 2.3 Setup on Ubuntu VM

The previous section also applies to deploying the application on an Ubuntu VM. This application uses a CI/CD pipeline. For the CD part, a bash script `rebuild_project.sh` is used to update the project. Additionally, you will need to set up a firewall for server protection and services for automation.

## 2.4 Setup on Docker

The simplest way to run the application is using Docker. To start the application, define the necessary environment variables and use the following commands:

- `docker compose up` - to start the application
- `docker compose down` - to stop the application

## 3. Tests

To run automated tests, set the `TEST_MODE` variable to `True` in the `app/settings.py` file. Then, you can use the command `pytest`.