import requests
import logging
from django.shortcuts import render, redirect
logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post('http://127.0.0.1:8000/api/token/', data={
            'username': username,
            'password': password,
        })

        if response.status_code == 200:
            tokens = response.json()
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            return redirect('dashboard')
        else:
            return render(request, 'frontend/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'frontend/login.html')


def dashboard_view(request):
    access_token = request.session.get('access_token')

    if not access_token:
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get('http://127.0.0.1:8000/pages/pages/', headers=headers)

    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 401:
        request.session.flush()
        return redirect('login')
    else:
        data = {"error": "Something went wrong."}

    return render(request, 'frontend/dashboard.html', {'data': data})


def logout_view(request):
    request.session.flush()
    return redirect('login')



def page_detail_view(request, page_id):
    access_token = request.session.get('access_token')
    if not access_token:
        logger.warning("No access token found in session.")
        return redirect('login')

    url = f'http://127.0.0.1:8000/pages/pages/{page_id}/'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    logger.info(f"Requesting page detail from: {url}")
    logger.info(f"Headers: {headers}")

    try:
        logger.info(f"call the page for id :{str(page_id)}")
        response = requests.get(url, headers=headers)
        logger.info(f"Response status: {response.status_code}")
        logger.debug(f"Response content: {response.text}")

        if response.status_code == 200:
            page_data = response.json()
        elif response.status_code == 401:
            logger.warning("Unauthorized - flushing session")
            request.session.flush()
            return redirect('login')
        else:
            logger.error("API returned non-200 response")
            page_data = {"error": "Something went wrong."}

    except requests.exceptions.RequestException as e:
        logger.exception("Request to API failed")
        page_data = {"error": "Request failed", "details": str(e)}

    return render(request, 'frontend/page_detail.html', {'page': page_data})