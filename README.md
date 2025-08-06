# Citizen Journal API

A modern, full-featured **Django + FastAPI** web API platform that empowers citizens to share, discuss, and verify news in a decentralized and transparent way.

---

## Overview

This project consists of two integrated backend services:

### 1. **Citizen Journal Backend (Django + PostgreSQL)**

A RESTful API for users (citizens) to create content, interact, and manage discussions. Key features include:

- **User Registration & Authentication** using JWT (access + refresh tokens)
- **Page System**: Each user owns a *Page* that acts as their personal hub
- **News Publishing**: Users can create *News* posts on their pages
- **Commenting & Replies**: News posts support comments with recursive replies
- **Discussions**: Each page has its own *Discussion* area with:
  - Multiple *Topics* (added by the page owner)
  - Each *Topic* supports *Questions* from other users
  - Each *Question* can be answered by others — enabling rich, threaded discussion

### 2. **Fake News Detection Service (FastAPI + ML)**

An intelligent microservice built with **FastAPI** that detects the authenticity of published news.

- Trained with **Logistic Regression**
- Achieved **99.25% accuracy** on test data
- Exposes an API endpoint used by the Django service to evaluate news reliability

---

##  Technologies

| Component        | Stack                              |
|------------------|-------------------------------------|
| API Framework    | Django REST Framework, FastAPI      |
| Authentication   | JWT (access/refresh) via `djangorestframework-simplejwt` |
| Database         | PostgreSQL                          |
| ML Model         | Scikit-learn, Logistic Regression   |
| Containerization | Docker + Docker Compose             |

---

## Authentication

- **JWT Token Auth**:
  - `/api/token/`: Login with username & password to receive access/refresh tokens
  - `/api/token/refresh/`: Refresh access token using refresh token
- **Registration**:
  - `/api/register/`: Register a new user along with their profile and avatar

---

## API Modules

- **Users**: Register, authenticate, manage profiles (including uploading photos)
- **Pages**: Each user gets a unique page to publish content
- **News**: News posts are created under pages and verified via ML service
- **Comments**: News posts support threaded comments and replies
- **Discussions**:
  - Topics (created by page owners)
  - Questions (asked by anyone)
  - Answers (provided by the community)
- **Fake News Detection**: Real-time validity scoring of news via FastAPI service

---

## Machine Learning Service

- Framework: **FastAPI**
- Model: **Logistic Regression**
- Accuracy: **99.25%** on test dataset
- Integration: Automatically called when a news item is submitted

---

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
