from django.urls import path
from .views import *
from .notify import *

urlpatterns = [
    path('', UserDashboardView.as_view(), name='user_dashboard'),
    # Admin Dashboard
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'), 
    path('sidebar/', sidebar_counts, name='sidebar'),
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/mark-as-read/<int:pk>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('navbar-notifications/', navbar_notifications, name='navbar_notifications'),
    # Purchases
    path('purchase/', PurchaseProductView.as_view(), name='purchase_list'),
    path('purchase/<int:pk>/update/', PurchachesUpdateView.as_view(), name='purchases_confirm'),  
    # Transactions
    path('transaction/', TransactionDetailView.as_view(), name='transaction_list'),
    path('transaction/<int:pk>/confirm', TransactionUpdateView.as_view(), name='transaction_confirm'),
]