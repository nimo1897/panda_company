from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Transaction, Purchase, Notification
from products.models import Vote
from customers.models import Profile, Company
from django.db.models import F
from decimal import Decimal



@receiver(post_save, sender=Vote)
def create_purchase_if_votes_enough(sender, instance, created, **kwargs):
    """
    Create a purchase if the product receives enough approved votes.
    """
    if created and instance.is_approved:
        product = instance.product
        total_customers = Profile.objects.count()
        product_vote = product.votes.filter(is_approved=True).count()  
        
        if product_vote >= 1:  # Check if the product has at least one approved vote
            if not Purchase.objects.filter(product=instance.product, buyer=instance.product.user).exists():
                Purchase.objects.create(
                    product=product,
                    buyer=product.user,  
                    total_amount=product.estimated_cost,
                    total_profit=product.estimated_profit,
                )

@receiver(post_save, sender=Purchase)
def create_transaction_on_admin_approval(sender, instance, created, **kwargs):
    """
    When admin_approved is set to True, create a new transaction and deduct the amount from the company balance.
    """
    if instance.admin_approved:  
        Transaction.objects.create(
            purchase=instance,
            amount=instance.total_amount,
            profit=instance.total_profit,
            buyer=instance.buyer,
            product=instance.product,
        )
        
        # Update the company balance
        company = Company.objects.first() 
        if company:
            company.total = F('total') - instance.total_amount  # Deduct the purchase amount
            company.funds_out = F('funds_out') + instance.total_amount
            company.save()  # Save the changes


        if instance.buyer and hasattr(instance.buyer, 'profile'):
            buyer_profile = instance.buyer.profile
            buyer_profile.funds_spent = F('funds_spent') + instance.total_amount
            buyer_profile.save()
        
        
        product_to_delete = instance.product

        # Delete the purchase record
        instance.delete()

        # Delete the product
        product_to_delete.delete()

@receiver(post_save, sender=Transaction)
def update_company_balance(sender, instance, created, **kwargs):
    """
    If the transaction is approved, update the company balance and distribute the profit among users.
    """
    if instance.approved:
        company = Company.objects.first()
        
        if company:
            company.total = F('total') + (instance.amount + instance.profit)  # Increase total balance by transaction amount
            company.profit = F('profit') + instance.profit  # Increase total profit
            company.funds_out = F('funds_out') - instance.amount
            company.save()
            company.refresh_from_db()

        total_customers = Profile.objects.count()
        if total_customers > 0:
            percent_profit = instance.profit * Decimal('0.20')  # 20% profit for the buyer
            the_new_profit = (instance.profit - percent_profit) / Decimal(total_customers)  # Distribute remaining profit
            
            # Update profit for the buyer
            if instance.buyer and hasattr(instance.buyer, 'profile'):
                buyer_profile = instance.buyer.profile
                buyer_profile.total_profit = F('total_profit') + percent_profit
                buyer_profile.total_payment = F('total_payment') + percent_profit
                buyer_profile.funds_spent = F('funds_spent') - instance.amount
                buyer_profile.save()
                buyer_profile.refresh_from_db()
                
                # 📢 Send notification to the buyer
                Notification.objects.create(
                    user=instance.buyer,
                    message=f"Your transaction of {instance.amount} has been approved. You received {percent_profit} + {the_new_profit} as profit."
                )
            
            # Update profit for all users
            Profile.objects.update(total_profit=F('total_profit') + the_new_profit)
            Profile.objects.all().update(total_payment=F('total_payment') + the_new_profit)
            
            # 📢 Send notification to all users except the buyer
            other_users = Profile.objects.exclude(user=instance.buyer)
            for profile in other_users:
                Notification.objects.create(
                    user=profile.user,
                    message=f"You received {the_new_profit} as distributed profit."
                )
            
        # Delete the transaction record after processing
        instance.delete()


    

@receiver(pre_delete, sender=Profile)
def remove_balance_from_company(sender, instance, **kwargs):
    percent_payment = instance.total_payment * Decimal('0.10')
    instance.total_payment -= percent_payment
    company = Company.objects.first()  
    if company:
        company.profit -= instance.total_profit
        company.balance -= instance.ballance  
        company.total -= instance.total_payment    
        company.save()