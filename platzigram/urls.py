"""
URL configuration for platzigram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django
from django.contrib import admin
from django.conf import settings # Importamos la libreria de "settings" para poder mostrar imagenes.
from django.conf.urls.static import static # Libreria para poder serviri imagenes en desarrollo.
from django.urls import path, include
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include(('posts.urls','posts'), namespace='posts')), # En la tupla incluimos al modulo "posts.urls" y la app "posts".
    path('users/', include(('users.urls','users'), namespace='users')), # En la tupla incluimos al modulo "users.urls" y la app "users".
    path('comment/', include(('comment.urls','comment'), namespace='comment')), # En la tupla incluimos al modulo "comment.urls" y la app "comment".
    path('message/', include(('directs.urls','directs'), namespace='directs')), # En la tupla incluimos al modulo "directs.urls" y la app "directs".
    
    
    #Password reset
    path(route='password_reset/', 
         view=auth_views.PasswordResetView.as_view(), 
         name='password_reset'
    ),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
