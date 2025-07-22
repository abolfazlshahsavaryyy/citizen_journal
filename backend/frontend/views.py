import requests
from django.shortcuts import render, redirect

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Send request to JWT token API
        response = requests.post('http://127.0.0.1:8000/api/token/', data={
            'username': username,
            'password': password,
        })

        if response.status_code == 200:
            tokens = response.json()
            # Save tokens in session
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']

            return redirect('front:dashboard')

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

    # Call your protected API endpoint
    response = requests.get('http://127.0.0.1:8000/pages/pages/', headers=headers)

    if response.status_code == 200:
        data = response.json()
    elif response.status_code == 401:
        # Token expired or invalid
        request.session.flush()
        return redirect('login')
    else:
        data = {"error": "Something went wrong."}

    return render(request, 'dashboard.html', {'data': data})


def logout_view(request):
    request.session.flush()
    return redirect('login')
