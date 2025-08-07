# CitizenJournal - A Twitter-like Web Application with Fake News and Hate Speech Detection

CitizenJournal is a modern, Twitter-inspired web API project that combines social interaction with powerful machine learning features. Built using Django as the main web framework and integrated with FastAPI for ML model serving, this application aims to provide a rich user experience with intelligent content moderation.

## Tech Stack

    Backend Framework: Django (main application)

    ML API Services: FastAPI

    Database: PostgreSQL

    Authentication: JWT (JSON Web Token)

    Asynchronous Tasks: Celery with RabbitMQ

## Machine Learning Features

#### This project includes two ML services:

    Fake News Detection

        Model: Logistic Regression

        Accuracy: 99.25% on test data

        Integrated with the News model (synchronous communication via FastAPI)

    Hate Speech Detection

        Model: CNN (Convolutional Neural Network)

        Accuracy: 81% on test data

        Integrated with the Comment model (synchronous communication via FastAPI)



## Modular Django Apps

### The project follows a modular Django architecture with several dedicated apps:

#### Page & News: Create pages and publish news within them.

#### Comment: Handles creation and moderation of comments, with hate speech scoring.

#### Discussion & Topic: Allows users to start discussions and organize them by topics.

#### Question & Answer: Enables Q&A functionality within discussions.

    Notification: Generates notifications asynchronously (e.g., when a news post is liked) using Celery and RabbitMQ.
# How to Use the API

Follow these steps to get the API service up and running locally:

### 1. Clone the Repository

```bash
git clone https://github.com/abolfazlshahsavaryyy/citizen_journal.git
cd citizen_journal/
```


### 2. Create and configure the .env file

```bash
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
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
