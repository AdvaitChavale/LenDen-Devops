terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.23.0"
    }
  }
}

provider "docker" {
  host = "tcp://127.0.0.1:2375"  # Use "tcp://127.0.0.1:2375" for Windows 
}

# Backend container (Python app or testing command)
resource "docker_container" "backend_replace" {
  image = "python:3.9"
  name  = "devops-backend"

  ports {
    internal = 8000
    external = 8000
  }

  volumes {
    host_path      = "${abspath("../backend/src/mysite")}"  # Correct path to the backend folder
    container_path = "/app"
  }

  command = ["sleep", "infinity"]  # Keep container alive for testing or run the app with appropriate command

  lifecycle {
    create_before_destroy = true
  }
}

# Frontend container (Nginx)
resource "docker_container" "frontend_replace" {
  image = "nginx:latest"
  name  = "devops-frontend"

  ports {
    internal = 80
    external = 8080
  }

  volumes {
    host_path      = "${abspath("../frontend/static")}"  # Correct path to the frontend folder
    container_path = "/usr/share/nginx/html"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# MongoDB container
resource "docker_container" "mongodb_replace" {
  image = "mongo:latest"
  name  = "devops-mongodb"

  ports {
    internal = 27017
    external = 27017
  }

  env = [
    "MONGO_INITDB_ROOT_USERNAME=root",
    "MONGO_INITDB_ROOT_PASSWORD=example"
  ]

  lifecycle {
    create_before_destroy = true
  }
}

# Mongo-Express container
resource "docker_container" "mongo_express_replace" {
  image = "mongo-express:latest"
  name  = "devops-mongo-express"

  ports {
    internal = 8081
    external = 8081
  }

  env = [
    "ME_CONFIG_MONGODB_ADMINUSERNAME=root",
    "ME_CONFIG_MONGODB_ADMINPASSWORD=example",
    "ME_CONFIG_BASICAUTH_USERNAME=root",
    "ME_CONFIG_BASICAUTH_PASSWORD=example"
  ]

  lifecycle {
    create_before_destroy = true
  }
}
