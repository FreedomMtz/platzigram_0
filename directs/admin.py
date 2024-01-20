# Django
from django.contrib import admin

# Models
from directs.models import Message

# Register your models here.


@admin.register(Message)
# Damos de alta al modelo llamado "Posts" para poder verlo en el ADMIN.
class ProfileAdmin(admin.ModelAdmin):
    """Posts admin."""
    list_display = ('pk', 'user', 'sender', 'reciepient', 'body', 'date',
                    'is_read')  # Modificamos la forma en que ADMIN mostraran los datos.
    # Declaramos campos que se podran buscar.
    search_fields = ('user', 'sender', 'reciepient', 'is_read')
