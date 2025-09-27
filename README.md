# CitizenJournal
## A Twitter-like Web Application with Fake News and Hate Speech Detection

CitizenJournal is a modern, Twitter-inspired web API project that combines social interaction with powerful machine learning features.
It is built using Django as the main backend framework and FastAPI for serving machine learning models. The application offers intelligent content moderation and social features such as pages, news, comments, discussions, Q&A, and notifications.

## Table of Contents## Table of Contents
- [CitizenJournal](#citizenjournal)
- [Description](#description)
  - [Django](#django)
  - [FastAPI](#fastapi)
  - [ASP.NET Core](#aspnet-core)
  - [API Types](#api-types)
    - [REST API](#rest-api)
    - [GraphQL API](#graphql-api)
    - [gRPC API](#grpc-api)
  - [Asynchronous Communication](#asynchronous-communication)
    - [Celery](#celery)
    - [RabbitMQ](#rabbitmq)
    - [Redis](#redis)
  - [Database Layer](#database-layer)
    - [PostgreSQL](#postgresql)
    - [SQL Server](#sql-server)
  - [Containerization](#containerization)
  - [Other Features](#other-features)
    - [Logging with Loguru](#logging-with-loguru)
    - [Request Throttling](#request-throttling)
    - [JWT Authentication](#jwt-authentication)
- [How to Use the API](#how-to-use-the-api)
  - [Linux User](#linux-user)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create and Configure the .env File](#2-create-and-configure-the-env-file)
    - [3. Start All Services](#3-start-all-services)
    - [4. Apply Database Migrations](#4-apply-database-migrations)
    - [5. Access the API](#5-access-the-api)



# Description
This project is a modular, multi-service backend platform for managing news, user interactions, and machine learning-powered content analysis. It leverages Django, FastAPI, and ASP.NET Core to provide robust API services. Key architectural highlights:

## Django:
Main backend framework for user management, news, comments, discussions, and GraphQL-based personalized news recommendations.

## FastAPI:
Microservices for machine learning features like fake news detection, hate speech detection, and summarization.

## ASP.NET Core:
Dedicated backend service exposing gRPC APIs for sharing news between users across different platforms. Django acts as a gRPC client to consume this service.

## API Types:

### REST API
(Django + FastAPI) for standard CRUD operations

### GraphQL API
(Django) for personalized news queries

### gRPC API
(ASP.NET) for high-performance inter-service communication

## Asynchronous Communication

### Celery:
Handles background tasks, such as notifications and news summarization.

### RabbitMQ:
Serves as the message broker for Celery workers.

### Redis:
Used as a cache layer and Celery result backend to improve performance.

## Database Layer

### PostgreSQL:
Primary relational database for Django and FastAPI services.

### SQL Server:
Used by the ASP.NET backend for storing shared news data.

## Containerization

All services are containerized with Docker and orchestrated using Docker Compose for easy deployment, scalability, and environment consistency.

## Other Features
### Logging with Loguru
The project uses Loguru for advanced logging

using interceptor for auto logging

### Request Throttling
The Django REST Framework is configured with throttling to prevent abuse
in this project the strcuture for throttling is as follows:
##### Global throttles:

Anonymous users: 50/day

Authenticated users: 2000/day

##### Scoped throttles for specific actions:

post_news: 5/minute

read_news: 100/minute

like_dislike_news: 3000/hour

create_page: 2/hour

create_topic: 10/minute

ask_question / answer_question: 5/minute

### JWT Authentication
Access tokens valid for 15 minutes, refresh tokens for 7 days.

Supports token rotation and blacklist after rotation.

Works with REST APIs (DRF Simple JWT) and GraphQL JWT integration.
## How to Use the API

Follow these steps to get the API service up and running locally:
## linux user

### 1. Clone the Repository

```bash
git clone https://github.com/abolfazlshahsavaryyy/citizen_journal.git
cd citizen_journal/
```


### 2. Create and configure the .env file

```bash
# .env.example
SECRET_KEY=please_set_a_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=your_broker_url

```

### 3. Start All Services
```bash
docker-compose up --build

```

### 4. Apply Database Migrations
```bash
docker-compose exec django python manage.py migrate

```


### 5. Access the API

    Django API: http://127.0.0.1:8000/

    Fake News Detection API (FastAPI): http://127.0.0.1:8001/

    Hate Speech API (FastAPI): https;//127.0.0.1:8002/

