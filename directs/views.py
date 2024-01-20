# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

# Models
from directs.models import Message
from django.contrib.auth.models import User

# Create your views here.


@login_required
def inbox(request):
    user = request.user  # Obtenemos al usuario actual.
    # Obtenemos todos los mensajes asociados al usuario actual.
    messages = Message.get_message(user=user)
    # Esta variable se utiliza para indicar con que usuario estamos hablando.
    active_direct = None
    # Esta variable guarda los mensajes asociados a la varibale anterior.
    directs = None

    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
        'unread_notifi': request.unread_notifi
    }
    
    return render(request, 'directs/inbox.html', context)


@login_required
def directs(request, username):
    user = request.user  # Obtenemos al usuario logeado
    # Obtenemos una lista de "users", "messages" y un contador que devuelve "get_message"
    messages = Message.get_message(user=user)
    # Definimos al usuario recipient con el "username" proporcionado por la URL/request.
    active_direct = username
    recipient = User.objects.get(username=active_direct)
    # Obtenemos todos los mensajes relacionados principalmente con el usuario actual y con el usuario del recipiente.
    directs = Message.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)  # Actualizamos el no leido a leido.

    for message in messages:
        # El request nos envia un username "que hemos seleccionado" y lo compara con el "recepient".
        if message['user'].username == username or user.username == active_direct:
            message['unread'] = 0  # Actualizamos el dato de no leidos a 0.

    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
        'unread_notifi': request.unread_notifi,
        'recipient': recipient
    }

    return render(request, 'directs/directs.html', context)


@login_required
def SendMessage(request):
    # Obtenemos al usuario logeado y lo guardamos en "from_user".
    from_user = request.user
    # Obtenemos al "remitente/username" que nos envia el form en el campo "to_user".
    to_user_username = request.POST.get('to_user')
    # Obtenemos al "mensaje" que nos envia el form en el campo "body".
    body = request.POST.get('body')
    # print("SendMessage")
    if request.method == "POST":  # Tambien, al recibir el form, pasa lo siguiente:
        # Definimos al campo "to_user/remitente" como obj "User" mediante "to_username"
        to_user = User.objects.get(username=to_user_username)
        # Llamamos a la función "send_message" con los campos obtenidos anteriormente.
        Message.send_message(from_user, to_user, body)
        # Construimos una "URL" con reverse.
        redirect_url = reverse('directs:direct', args=[to_user_username])

        context = {
            'unread_notifi': request.unread_notifi
        }
        # Y redirigimos a "url direct" que es el chat personal.
        return redirect(redirect_url, context)
    else:
        pass  # No hagas algo


@login_required
def UserSearch(request):
    query = request.GET.get('q')
    context = {'unread_notifi': request.unread_notifi}

    if query:
        users = User.objects.filter(Q(username__icontains=query))
        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            'unread_notifi': request.unread_notifi
        }
        
    return render(request, 'directs/search.html', context)


@login_required
def NewMessage(request, username):
    from_user = request.user
    body = ""
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect("directs:userSearch")
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    redirect_url = reverse('directs:direct', args=[to_user])
    context = {'unread_notifi': request.unread_notifi}
    
    return redirect(redirect_url, context)


@login_required
def DeleteMessage(request, username):
    user = request.user
    # print("eliminacion de perfil1")
    reciepient = User.objects.get(username=username)
    if request.method == 'POST':
        messages = Message.objects.filter(user=user, reciepient=reciepient)
        messages.delete()
        
        return redirect('directs:message')  # Reemplaza con tu URL de inicio
    
    context = {
        'unread_notifi': request.unread_notifi,
        'recipient': reciepient
    }
    
    return render(request, 'directs/delete_message.html', context)
