# Django
from django.contrib import admin

#Models
from directs.models import Message

# Register your models here.
@admin.register(Message)
class ProfileAdmin(admin.ModelAdmin): # Damos de alta al modelo llamado "Posts" para poder verlo en el ADMIN.
    """Posts admin."""
    list_display = ('pk','user','sender','reciepient','body','date','is_read') # Modificamos la forma en que ADMIN mostraran los datos.
    search_fields = ('user','sender','reciepient','is_read') # Declaramos campos que se podra buscar.
    
 