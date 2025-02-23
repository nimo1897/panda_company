from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('edit-profile/', UserEditView.as_view(), name='edit_profile'),
    # Password change URL
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    # Optional success page (after successful password change)
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'), 
]