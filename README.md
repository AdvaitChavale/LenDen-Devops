# LenDen-Devops
# README

## Overview

This project is a full-stack minimalistic to-do list application designed with a modular structure to ensure scalability, maintainability, and ease of deployment. The application is containerized using Docker and includes the following components:

- **Backend**: A Python-based backend implemented using a virtual environment (myenv) and a structured file hierarchy.
 Please make a virtual environment on your own and name it "myenv".
- **Frontend**: A static HTML frontend served via its own container with nginx dockerized webserverb at port 80.
- **Database**:
  - **MongoDB**: A database containerized and linked to the application.
  - **Mongo-Express**: A web-based administrative interface for MongoDB.
Make 2 folders containing .env file with both the above names for database (it contains Id & password for your Mongodb)
eg-
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example

- **Terraform**: Infrastructure as Code (IaC) for provisioning. Terraform docker image was pulle (you need to do it manually)

The project uses Docker Compose to manage the multi-container setup, ensuring seamless communication between components.

## File Structure

```
- backend/ (separate container: devops-backend)
  - myenv/ (Python virtual environment)
    - include/
    - lib/site-packages/
    - scripts/
  - .gitignore
  - pyenv.cfg
  - src/mysite/
    - __init__.py
    - main.py
  - .env
  - Dockerfile
  - pyproject.toml
  - requirements.txt

- frontend/ (separate container: devops-frontend)
  - static/
  - index.html
  - Dockerfile

- mongo-express/ (separate container: devops-mongo-express)
  - .env

- mongodb/ (separate container: devops-mongodb)
  - .env

- terraform/ (folder for IaC configurations)
  - main.tf
  - variables.tf
  - outputs.tf
  - provider.tf

- myenv/ (separate folder outside backend folder)
- .gitignore
- docker-compose.yml
```
## Instructions for Building and Running the Application Locally

### Prerequisites

- Docker
- Docker Compose
- Terraform

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

3. Access the application:

   - **Backend**: The backend service will be available at `http://localhost:8000`.
   - **Frontend**: The frontend will be accessible at `http://localhost:80`.
   - **Mongo-Express**: Access Mongo-Express at `http://localhost:8081`.

4. To stop the application:

   ```bash
   docker-compose down
   ```

## Deployment Steps

1. Ensure that the environment variables in `.env` files for all services are correctly configured.
2. Push the Docker images to your container registry:
   ```bash
   docker-compose push
   ```
3. Deploy the `docker-compose.yml` file to your production environment.
   ```bash
   docker-compose up -d
   ```
4. Use Terraform to provision the necessary infrastructure:
   ```bash
   terraform init
   terraform apply
   ```
5. Verify that all containers are running and accessible.

## Monitoring Instructions

### Backend Logs

Monitor the backend container logs:

```bash
docker logs <backend-container-name>
```

### Frontend Logs

Monitor the frontend container logs:

```bash
docker logs <frontend-container-name>
```

### MongoDB Logs

Monitor the MongoDB container logs:

```bash
docker logs <mongodb-container-name>
```

### Mongo-Express Logs

Monitor the Mongo-Express container logs:

```bash
docker logs <mongo-express-container-name>
```

### Docker Container Status

Check the status of all containers:

```bash
docker ps
```

### Terraform Logs

Monitor Terraform operations:

```bash
terraform show
```

