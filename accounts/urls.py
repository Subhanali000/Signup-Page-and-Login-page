from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
     path('blog/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),

    path('blog/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
   
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),  # Blog detail page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)