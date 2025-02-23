from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserEditForm, CustomPasswordChangeForm
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, FormView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import redirect






@method_decorator(never_cache, name='dispatch')
class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'profile/edit_profile.html'  # Template to render the form
    success_url = reverse_lazy('user_dashboard')  # Redirect to profile page after saving changes

    def get_object(self, queryset=None):
        # This ensures we get the current user's User object
        return self.request.user

    
    
    
@method_decorator(never_cache, name='dispatch')
class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'profile/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')  # Redirect after password change success

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        # If the form is valid, update the user's password
        user = form.save()
        update_session_auth_hash(self.request, user)  # Keep the user logged in after password change
        return redirect(self.success_url)
    
    
    
@method_decorator(never_cache, name='dispatch')   
class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'profile/password_change_done.html'