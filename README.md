# CitizenJournal
## A Twitter-like Web Application with Fake News and Hate Speech Detection

CitizenJournal is a modern, Twitter-inspired web API project that combines social interaction with powerful machine learning features.
It is built using Django as the main backend framework and FastAPI for serving machine learning models. The application offers intelligent content moderation and social features such as pages, news, comments, discussions, Q&A, and notifications.
## Tech Stack

    Backend Framework: Django (main application)

    ML API Services: FastAPI

    Database: PostgreSQL

    Authentication: JWT (JSON Web Token)

    Asynchronous Tasks: Celery with RabbitMQ

## Machine Learning Features

This project includes two machine learning services:
### Fake News Detection

    Model: Logistic Regression

    Accuracy: 99.25% on test data

    Integration: Synchronous communication with the News model via FastAPI

### Hate Speech Detection

    Model: Convolutional Neural Network (CNN)

    Accuracy: 86% on test data

    Integration: Synchronous communication with the Comment model via FastAPI

### Summarizing Model: sshleifer/distilbart-cnn-12-6
    In this service, we configured a lightweight summarization model — sshleifer/distilbart-cnn-12-6
    model url : https://huggingface.co/sshleifer/distilbart-cnn-12-6
    its a Lightweight,Faster inference,Lower resource usage and Hight accurate model
    its used to summaried news text 

## Modular Django Apps

The project is organized into multiple Django apps for better modularity and scalability:
###  Page & News

    Developed a system to create and manage pages.

    Implemented functionality to publish news articles under each page.

    Integrated a machine learning model to detect fake news.

    Designed a GraphQL endpoint to provide personalized "For You" news recommendations.

    Implemented an advanced search feature on news articles, allowing users to query by keywords

### Comment

    Add and manage comments on news

    Score comments using the hate speech detection service

    self referenc relation as reply on Comment

### Discussion & Topic

    Start and participate in discussions

    Organize conversations under various topics

### Question & Answer

    Ask and answer questions within discussions

    Community-style interaction

### Notification

    Send real-time notifications (e.g., news likes)

    Asynchronous task handling with Celery and RabbitMQ

## Backend Implementation

### Authentication:
    Implemented JWT authentication with both access and refresh tokens for secure user sessions.
### Celery: 
    We use Celery to handle asynchronous tasks within the application. It is utilized in two key areas:
    Sending notifications asynchronously to improve responsiveness.
    Summarizing news text in the background, offloading heavy NLP tasks from the main API. 
    
### RabbitMQ: 
    RabbitMQ is used as the message broker for Celery workers, enabling reliable task queuing
    and communication between services.
### redis:
    Redis serves as a temporary in-memory data store, used to cache summarized news text after
    it has been processed by the summarization model — improving response times and
    reducing redundant computations.

### GraphQL Integration:
    Configured GraphQL to use the same authentication tokens as the rest of the system,
    ensuring consistent and secure access control across all endpoints.
    GraphQL is used to fetch personalized news recommendations for each user,
    providing flexible and efficient data querying tailored to individual preferences.

### Database Design:
    Built with PostgreSQL, including a well-structured Entity Relationship Diagram (ERD) to define and
    enforce complete model relationships.

### Django ORM:
    Utilized Django ORM to perform advanced queries and manage data efficiently.

### Django REST Framework (DRF):
    Fully integrated with DRF using views, services, and serializers for clean and modular 
    API development.

### Containerization:
    All services are containerized with Docker and orchestrated using Docker Compose for 
    easy deployment and scalability.
### Signal
    Configure a signal decorator to automatically create user information, user pages, and discussion 
    threads whenever a new user is created. 
### Logging
    Use Loguru with an InterceptHandler to capture and redirect standard logs, while also defining
    custom loggers for specialized application behaviors.

## Docker Compose Services:
### PostgreSQL (db)
Image: postgres:15

Acts as the primary relational database for the Django application and other services.

Configured via an .env file for credentials and database settings.

Includes a healthcheck to ensure the database is ready before dependent services start.

Ports:5433:5432

### Django (django):
Framework: Django (Python)

Serves as the main backend and API layer, handling business logic, authentication, and orchestration of other services.

Automatically applies database migrations on startup.

Loads configuration from environment variables and .env.

Ports: 8000:8000

### Celery (celery):
Purpose: Asynchronous task queue worker.

Executes long-running or background tasks such as:

Sending notifications
Summarizing news text

Depends on PostgreSQL, RabbitMQ, Redis, and the Summarizer service.

Waits a few seconds on startup to ensure all services are ready.

### FastAPI Services
#### Fake News Detection (fastapi):
A FastAPI microservice for detecting fake news.

Connects to the same PostgreSQL database as Django.

Ports: 8001:8001

#### Hate Speech Detection (hate_speech_api):
Provides a dedicated API to detect and filter hate speech in content.

Lightweight FastAPI service, independently deployable.

Ports: 8002:8000

#### Summarizer Service (summarizer)

A FastAPI microservice for text summarization.

Uses a lightweight transformer model (sshleifer/distilbart-cnn-12-6)
Ports: 8003:8003

### RabbitMQ (rabbitmq)
Message broker for Celery task queue.

Facilitates communication between Django and background workers.

Includes a web-based management UI.

Ports:

5672 → message broker

15672 → management dashboard

### Redis (redis)

In-memory key-value store used as:

A Celery backend for task result storage.

A cache layer for storing summarized news text temporarily, improving performance.

Ports: 6379:6379

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

