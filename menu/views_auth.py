"""
Frontend authentication views for 60 Seconds to Napoli
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json


def login_page(request):
    """Display login page and handle login form submission"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Set session expiry based on remember me
            if not remember:
                request.session.set_expiry(0)  # Browser close
            
            # Redirect to next page or home
            next_url = request.GET.get('next', 'home')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            return render(request, 'auth/login.html', {
                'error': 'Invalid username or password. Please try again.'
            })
    
    return render(request, 'auth/login.html')


def register_page(request):
    """Display registration page and handle registration form submission"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        terms = request.POST.get('terms')
        
        errors = []
        
        # Validation
        if not all([first_name, last_name, username, email, password, password_confirm]):
            errors.append('All fields are required.')
        
        if password != password_confirm:
            errors.append('Passwords do not match.')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        
        if User.objects.filter(email=email).exists():
            errors.append('Email is already registered.')
        
        if not terms:
            errors.append('You must accept the Terms of Service.')
        
        if errors:
            return render(request, 'auth/register.html', {'errors': errors})
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Auto login
        login(request, user)
        messages.success(request, f'Welcome to 60 Seconds to Napoli, {first_name}!')
        return redirect('home')
    
    return render(request, 'auth/register.html')


def logout_page(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def account_page(request):
    """Display user account page"""
    return render(request, 'auth/account.html')


@login_required
@require_POST
@csrf_protect
def update_profile(request):
    """Handle profile update via AJAX"""
    try:
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_POST
@csrf_protect
def change_password(request):
    """Handle password change via AJAX"""
    try:
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not user.check_password(current_password):
            return JsonResponse({
                'success': False,
                'error': 'Current password is incorrect.'
            }, status=400)
        
        if new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'error': 'New passwords do not match.'
            }, status=400)
        
        if len(new_password) < 8:
            return JsonResponse({
                'success': False,
                'error': 'Password must be at least 8 characters long.'
            }, status=400)
        
        user.set_password(new_password)
        user.save()
        
        # Re-authenticate to maintain session
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Password changed successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
