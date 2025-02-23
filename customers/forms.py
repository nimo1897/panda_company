from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import PasswordChangeForm




    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Optionally, add validation for email if needed
        return email
    
    
    


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom classes to the fields dynamically
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})