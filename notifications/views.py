# Django.
from django.shortcuts import render, redirect
from django.db.models import Q

# Models.
from notifications.models import Notification

# Create your views here.


def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    context = {
        'notifications': notifications,
        'unread_notifi': request.unread_notifi
    }
    return render(request, 'notifications/notifi.html', context)


def DeleteNotifications(request, noti_id):
    user = request.user
    delete_noti = Notification.objects.filter(id=noti_id, user=user)
    delete_noti.delete()

    return redirect('notifications:showNotifi')

#Context processor
def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(
            Q(user=request.user,is_seen=False) & ~Q(sender=request.user)).count()
        
    return {'count_notifications': count_notifications}
