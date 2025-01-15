from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or a success page
        else:
            # If form is not valid, display errors
            messages.error(request, "There was an error with your form submission.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            # If form is not valid, add an error message
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logging out
