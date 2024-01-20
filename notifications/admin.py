# Django
from django.contrib import admin

# Modules
from notifications.models import Notification

# Register your models here.


@admin.register(Notification)
# Damos de alta al modelo llamado "Posts" para poder verlo en el ADMIN.
class ProfileAdmin(admin.ModelAdmin):
    """Notification admin."""
    list_display = ('pk', 'user', 'sender', 'post', 'notification_type', 'text_preview',
                    'date', 'is_seen')  # Modificamos la forma en que ADMIN mostraran los datos.
    # Declaramos campos que se podra buscar.
    search_fields = ('user', 'sender', 'post', 'notification_type', 'is_seen')
