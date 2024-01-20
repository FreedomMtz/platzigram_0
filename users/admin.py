"""User admin classes."""
# Django.
# Libreria para delegar al "ADMIN" a otro modelo.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models.
# Importamos al modelo User para poder delegar al "ADMIN" al modelo Profile.
from django.contrib.auth.models import User
from users.models import Profile, Follow

# Register your models here.


@admin.register(Profile)
# Damos de alta al modelo llamado "Profile" para poder verlo en el ADMIN.
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""
    list_display = ('pk', 'user', 'phone_number', 'website',
                    'picture')  # Modificamos la forma en que ADMIN mostraran los datos.
    # Este comnado nos permite acceder a los datos para modificarlos.
    list_display_links = ('pk', 'user')
    # Con este atributo podemos modificarlos sin tener que ir a detalles.
    list_editable = ('phone_number', 'website', 'picture')
    # Declaramos campos que se podra buscar.
    search_fields = ('user__username', 'user__email',
                     'user__first_name', 'user__last_name', 'phone_number')

    list_filter = (
        'user__is_active',
        'user__is_staff',
        'created',
        'modified'
    )  # Creamos una seccion de filtrado de datos en donde los parametros a filtrar son del modelo "Profile" y "Users".

    fieldsets = (
        ('Profile', {
            'fields':
                (('user', 'picture'),),
        }),
        ('Extra info', {
            'fields': (
                ('website', 'phone_number'),
                ('biography'),
            ),
        }),
        ('Metadata', {
            'fields': (('created', 'modified'),),
        })

    )  # Seccion personalizada de como y que mostrar en los detalles del modelo "Profile".

    # Estos datos no son campos, pues los asigna el sistema y solo son de lectura.
    readonly_fields = ('created', 'modified',)


class ProfileInLine(admin.StackedInline):
    """Profile in-line admin for user."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin."""
    inlines = (ProfileInLine,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Follow)
# Damos de alta al modelo llamado "Follow" para poder verlo en el ADMIN.
class ProfileAdmin(admin.ModelAdmin):
    """Posts admin."""
    list_display = (
        'pk', 'follower', 'following')  # Modificamos la forma en que ADMIN mostraran los datos.
    list_filter = (
        'follower',
        'following'
    )
