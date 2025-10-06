from django.shortcuts import render, redirect
import requests
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        logger.info("Attempting login for user: %s", username)

        try:
            response = requests.post(
                "http://django:8000/api/token/",
                data={"username": username, "password": password},
                timeout=5
            )
        except requests.exceptions.RequestException as e:
            logger.error("Error connecting to backend /api/token/: %s", e)
            return render(request, "frontapp/login.html", {"error": "Backend not reachable."})

        logger.info("Login API status: %s", response.status_code)
        logger.debug("Login API response: %s", response.text)

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get("access")
            refresh_token = tokens.get("refresh")

            if not access_token:
                logger.error("Access token missing from response!")
                return render(request, "frontapp/login.html", {"error": "Invalid token response."})

            # ✅ Save both tokens in session
            request.session["access_token"] = access_token
            request.session["refresh_token"] = refresh_token
            logger.info("Tokens stored in session. Redirecting to home.")

            return redirect("home")
        else:
            logger.warning("Login failed. Status: %s Response: %s", response.status_code, response.text)
            return render(request, "frontapp/login.html", {"error": "Invalid credentials"})

    return render(request, "frontapp/login.html")


def home_view(request):
    logger.info("Home view accessed")

    access_token = request.session.get("access_token")
    if not access_token:
        logger.warning("Access token not found in session. Redirecting to login.")
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get("http://django:8000/pages/news/", headers=headers, timeout=5)
        logger.info("News API status: %s", response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error("Error connecting to backend /pages/news/: %s", e)
        return render(request, "frontapp/home.html", {"news_list": [], "error": "Backend not reachable."})

    news_list = response.json() if response.status_code == 200 else []

    if response.status_code != 200:
        logger.error("Failed to load news. Response: %s", response.text)

    return render(request, "frontapp/home.html", {"news_list": news_list})

def news_detail_view(request, news_id):
    access_token = request.session.get("access_token")  # ✅ use the same key as in login
    if not access_token:
        return redirect("login")  # Redirect if not logged in

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"http://django:8000/pages/news/{news_id}/", headers=headers, timeout=5)
        response.raise_for_status()  # Raise exception for non-200 responses
        news = response.json()
    except requests.exceptions.RequestException as e:
        news = None
        print("Error fetching news details:", e)

    return render(request, "frontapp/news_details.html", {"news": news})


def news_comments_view(request, news_id):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"http://django:8000/comment/news-comments/{news_id}/", headers=headers, timeout=5)
        response.raise_for_status()
        comments = response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching comments: %s", e)
        comments = []

    # Pass news_id to template so we can link back
    return render(request, "frontapp/news_comments.html", {"comments": comments, "news_id": news_id})

def comment_detail_view(request, comment_id):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(f"http://django:8000/comment/comment/{comment_id}/", headers=headers, timeout=5)
        response.raise_for_status()
        comment = response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching comment details: %s", e)
        comment = None

    return render(request, "frontapp/comment_detail.html", {"comment": comment})

