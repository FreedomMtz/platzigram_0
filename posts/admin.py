from django.contrib import admin

from posts.models import Post, Like

# Register your models here.
@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin): # Damos de alta al modelo llamado "Posts" para poder verlo en el ADMIN.
    """Posts admin."""
    list_display = ('pk','user','profile','title','photo','likes') # Modificamos la forma en que ADMIN mostraran los datos.
    search_fields = ('user__username','user__email') # Declaramos campos que se podra buscar.
    list_editable = ('likes','title')

@admin.register(Like)
class ProfileAdmin(admin.ModelAdmin): # Damos de alta al modelo llamado "Follow" para poder verlo en el ADMIN.
    """Posts admin."""
    list_display = ('pk','user','post') # Modificamos la forma en que ADMIN mostraran los datos.
    
