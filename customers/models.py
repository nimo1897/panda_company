from django.db import models
from dashboards.models import Company
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import F



class Profile(models.Model):
    choices = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ballance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    funds_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gender = models.CharField(max_length=10, choices=choices, default='male')
    date_created = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.user.username




class Payment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payments')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=now)
    sum_of_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Save the payment instance first
        super().save(*args, **kwargs)  
        
        # Update company balance after saving the payment
        self.update_company_balance()

        # Update the sum_of_payments after saving the payment
        self.update_sum_of_payments()

        # Save the payment instance again to persist the updated sum_of_payments
        super().save(*args, **kwargs)

    def update_sum_of_payments(self):
        # Calculate and update the sum_of_payments
        self.sum_of_payments = self.profile.ballance + self.amount

    def update_company_balance(self):
        company = Company.objects.first() 
        if company:
            company.balance = F('balance') + self.amount
            company.total = F('total') + self.amount
            company.save()
            


    def __str__(self):
        return f"{self.profile.user.username}"
    
    
    
    
    
