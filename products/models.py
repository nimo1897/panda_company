from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Product(models.Model):
    choice_state = (('sold', 'Sold'), ('unsold', 'Unsold'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')  
    description = models.TextField()    
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)    
    estimated_profit = models.DecimalField(max_digits=10, decimal_places=2)  
    estimated_time = models.IntegerField()
    state = models.CharField(max_length=20, choices=choice_state, default='unsold')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    

    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')  
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Comment by {self.user} on {self.product.name}"




class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='votes')  
    is_approved = models.BooleanField(default=False)    

    def __str__(self):
        return f"Vote by {self.user} on {self.product.name}"





