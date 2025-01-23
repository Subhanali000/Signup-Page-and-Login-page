# myproject/urls.py
from django.urls import path
from accounts import views  # Import views from accounts app
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup, name='signup'),  # Signup page
     path('logout/', views.logout_view, name='logout'),  # Add this line
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor dashboard
    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),  # Patient dashboard
     path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),

    path('create_blog/', views.create_blog, name='create_blog'),  # Create blog
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Blog detail URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)