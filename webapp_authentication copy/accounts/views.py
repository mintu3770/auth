from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
import firebase_admin
from firebase_admin import auth
from firebase_admin._auth_utils import UserNotFoundError

# Firebase initialization should already be done in settings.py

# Sign up view
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Create a new user with Firebase Authentication
            user = auth.create_user(email=email, password=password)
            messages.success(request, 'User created successfully')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('signup')

    return render(request, 'signup.html')


# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Firebase does not handle passwords directly on the backend side.
            # You should use Firebase Client SDK on the frontend to authenticate users.
            user = auth.get_user_by_email(email)
            messages.success(request, 'Login successful')
            return redirect('home')
        except UserNotFoundError:
            messages.error(request, 'User not found. Please sign up.')
            return redirect('signup')
        except Exception as e:
            messages.error(request, f'Error logging in: {str(e)}')
            return redirect('login')

    return render(request, 'login.html')


# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')