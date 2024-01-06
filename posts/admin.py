from django.contrib import admin

from posts.models import Post

# Register your models here.
@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin): # Damos de alta al modelo llamado "Posts" para poder verlo en el ADMIN.
    """Posts admin."""
    list_display = ('pk','user','profile','title','photo') # Modificamos la forma en que ADMIN mostraran los datos.
    
    search_fields = ('user__username','user__email') # Declaramos campos que se podra buscar.
    