from django.views.generic import ListView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  Notification
from django.shortcuts import redirect
from django.contrib import messages




@method_decorator(never_cache, name='dispatch')
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        notifications = Notification.objects.filter(user=self.request.user).order_by('-created_at')

        notifications.filter(is_read=False).update(is_read=True)

        return notifications



def mark_notification_as_read(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # get the notification
        notification = Notification.objects.get(id=pk, user=request.user)
        
        # update is_read to True
        notification.is_read = True
        notification.save()

        # back to product details
        if notification.product:
            return redirect('product_details', pk=notification.product.id)
    except Notification.DoesNotExist:
        
        messages.error(request, "Notification not found or you don't have permission to access it.")

    # back to notifications page
    return redirect('notifications')



def navbar_notifications(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'unread_notifications_count': unread_notifications_count,
            'unread_notifications': unread_notifications
        }
    return {
        'unread_notifications_count': 0, 
        'unread_notifications': []
    }