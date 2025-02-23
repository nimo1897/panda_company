from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]