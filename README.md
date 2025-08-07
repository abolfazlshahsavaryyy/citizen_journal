📰 CitizenJournal
A Twitter-like Web Application with Fake News and Hate Speech Detection

CitizenJournal is a modern, Twitter-inspired web API project that combines social interaction with powerful machine learning features.
It is built using Django as the main backend framework and FastAPI for serving machine learning models. The application offers intelligent content moderation and social features such as pages, news, comments, discussions, Q&A, and notifications.
⚙️ Tech Stack

    Backend Framework: Django (main application)

    ML API Services: FastAPI

    Database: PostgreSQL

    Authentication: JWT (JSON Web Token)

    Asynchronous Tasks: Celery with RabbitMQ

🧠 Machine Learning Features

This project includes two machine learning services:
🔍 Fake News Detection

    Model: Logistic Regression

    Accuracy: 99.25% on test data

    Integration: Synchronous communication with the News model via FastAPI

💬 Hate Speech Detection

    Model: Convolutional Neural Network (CNN)

    Accuracy: 81% on test data

    Integration: Synchronous communication with the Comment model via FastAPI

🧱 Modular Django Apps

The project is organized into multiple Django apps for better modularity and scalability:
📄 Page & News

    Create pages

    Publish news under each page

💬 Comment

    Add and manage comments on news

    Score comments using the hate speech detection service

🗣️ Discussion & Topic

    Start and participate in discussions

    Organize conversations under various topics

❓ Question & Answer

    Ask and answer questions within discussions

    Community-style interaction

🔔 Notification

    Send real-time notifications (e.g., news likes)

    Asynchronous task handling with Celery and RabbitMQ


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
