from django import forms
from .models import Transaction, Purchase
from customers.models import Payment, Profile
from .models import Company


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'buyer', 'total_amount', 'total_profit', 'admin_approved']

        
        
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['purchase', 'product', 'buyer', 'amount', 'profit', 'approved']
        
        
        

class PaymentForm(forms.ModelForm):
    profile = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        label="Select Client",
        required=True
    )

    class Meta:
        model = Payment
        fields = ['profile', 'amount', 'payment_date']
        widgets = {
            'profile': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
        
        
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'total', 'balance', 'funds_out', 'profit']