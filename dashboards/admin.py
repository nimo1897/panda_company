from django.contrib import admin
from .models import Company, Purchase, Transaction, Notification




admin.site.register(Company)
admin.site.register(Purchase)
admin.site.register(Transaction)
admin.site.register(Notification)
