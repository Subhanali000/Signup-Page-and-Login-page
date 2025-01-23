from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, BlogForm
from .models import Blog
from django.core.exceptions import ValidationError

# Home page view
def home(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.all()  # Display all blogs for authenticated users
    else:
        blogs = Blog.objects.filter(is_draft=False)  # Show only published blogs for unauthenticated users
    return render(request, 'accounts/home.html', {'blogs': blogs})

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users to home page

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_based_on_user_type(user)  # Redirect based on user type
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Sign up view
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Create and save the user
            login(request, user)  # Log the user in
            return redirect_based_on_user_type(user)  # Redirect based on user type
        else:
            messages.error(request, "There was an error with your form submission.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

# Redirect users based on user type (doctor or patient)
def redirect_based_on_user_type(user):
    if user.user_type == 'doctor':
        return redirect('doctor_dashboard')  # Redirect to the doctor's dashboard
    elif user.user_type == 'patient':
        return redirect('patient_dashboard')  # Redirect to the patient's dashboard
    else:
        return redirect('home')  # Fallback to home if user type is unknown

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Doctor dashboard view (requires login)
@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return redirect('home')  # Restrict non-doctor users from accessing this view
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'accounts/doctor_dashboard.html', {'user': request.user, 'blogs': blogs})

# Patient dashboard view (requires login)
@login_required
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        return redirect('home')  # Restrict non-patient users from accessing this view
    blogs = Blog.objects.filter(is_draft=False).order_by('-created_at')  # Only show published blogs
    return render(request, 'accounts/patient_dashboard.html', {'user': request.user, 'blogs': blogs})

# Create a blog (restricted to doctors only)
@login_required
def create_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')[:15]
        image = request.FILES.get('image')
        category = request.POST.get('category')[:15]
        summary = request.POST.get('summary')[:15]
        content = request.POST.get('content')[:15]
        is_draft = request.POST.get('is_draft') == "on"
        summary_word_count = len(summary.split())
        if summary_word_count > 15:
            raise ValidationError("Summary cannot exceed 15 words.")
        blog = Blog.objects.create(
            title=title,
            image=image,
            category=category,
            summary=summary,
            content=content,
            is_draft=is_draft,
            author=request.user,
        )
        
        messages.success(request, "Blog saved successfully.")
        return redirect('doctor_dashboard')
    return render(request, 'accounts/create_blog.html')

# Blog detail view
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'accounts/blog_detail.html', {'blog': blog})

# Delete blog view
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
    else:
        messages.error(request, "Invalid request.")
    return redirect('doctor_dashboard')

# Edit blog view
@login_required
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Ensure only the author (doctor) can edit the blog
    if blog.author != request.user:
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect('doctor_dashboard' if request.user.user_type == 'doctor' else 'patient_dashboard')

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.summary = request.POST.get('summary')
        blog.content = request.POST.get('content')
        blog.category = request.POST.get('category')

        # Handle optional image update
        if 'image' in request.FILES:
            blog.image = request.FILES['image']

        # Handle visibility update (Draft or Published)
        visibility = request.POST.get('visibility')
        if visibility == 'draft':
            blog.is_draft = True
        else:
            blog.is_draft = False

        blog.save()
        messages.success(request, "Blog updated successfully.")
        return redirect('doctor_dashboard' if request.user.user_type == 'doctor' else 'patient_dashboard')

    return render(request, 'accounts/edit_blog.html', {'blog': blog})
