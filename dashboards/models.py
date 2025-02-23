from django.db import models
from products.models import Product
from django.contrib.auth.models import User



# Company
class Company(models.Model):
    name = models.CharField(max_length=100, default='Panda-Company')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    funds_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return "Company Balance"




# Purchase
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # The product being purchased
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the purchase
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total amount of the purchase
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total profit from the purchase
    purchased_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the purchase was made
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Purchase of {self.product.name} by {self.buyer.username}"



# Transaction
class Transaction(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.SET_NULL, null=True, blank=True, related_name="transaction")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)  # the product can be empty if the product was deleted
    buyer = models.ForeignKey(User, on_delete=models.CASCADE) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)  
    transaction_date = models.DateTimeField(auto_now_add=True) 
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Transaction for {self.product.name if self.product else 'Deleted Product'} by {self.buyer.username} - {self.amount} TND"
    
    
    
# Notification 
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  
    message = models.TextField() 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)    
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"