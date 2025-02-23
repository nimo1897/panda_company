from django.contrib.auth.views import LoginView
from django.shortcuts import render



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # specify your custom template
    redirect_authenticated_user = True  # Redirect to the next page if the user is already logged in

    def form_valid(self, form):
        # This method is called if the form is valid
        # You can add extra functionality here, like logging or updating user activity
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Add custom context to the template if needed
        context = super().get_context_data(**kwargs)
        context['custom_message'] = 'Please login to access your account'
        return context
