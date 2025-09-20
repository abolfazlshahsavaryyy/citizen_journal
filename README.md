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

### GraphQL Integration:
    Configured GraphQL to use the same authentication tokens, ensuring consistent access control.

### Database Design:
    Built with PostgreSQL, including a well-structured Entity Relationship Diagram (ERD) to define and enforce complete model relationships.

### Django ORM:
    Utilized Django ORM to perform advanced queries and manage data efficiently.

### Django REST Framework (DRF):
    Fully integrated with DRF using views, services, and serializers for clean and modular API development.

### Containerization:
    All services are containerized with Docker and orchestrated using Docker Compose for easy deployment and scalability.
# How to Use the API

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

