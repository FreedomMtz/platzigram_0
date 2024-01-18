#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

#Models
from directs.models import Message
from django.contrib.auth.models import User

# Create your views here.

@login_required
def inbox(request):
    user = request.user #Obtenemos al usuario actual
    messages = Message.get_message(user=user) #Obtenemos todos los mensajes asociados al usuario actual.
    active_direct = None #Esta variable se utiliza para indicar con que usuario estamos hablando.
    directs = None #Esta variable guarda los mensajes asociados a la varibale anterior.
    #print(messages)
    #if messages: #Si hay mensajes entonces
        #message = messages[0] #Comenzamos con el primer elemento
        #active_direct = message['user'].username #Definimos al usuario actual con el que conversamos
        #directs = Message.objects.filter(user=user, reciepient=message['user']) # Ibtenemos todos los mensajes asociados al usuario actual y al recipiente.
        #directs.update(is_read=True) #Cambiamos el estado de "no leido" a "leido"
        
        #for message in messages: #Iteramos todos los mensajes obtenidos
            #if message['user'].username == active_direct: #Si el usuario de cada mensaje obtenido es igual al del recipiente 
                #message['unread'] = 0 #Reiniciamos el contador de emensajes no leidos.
    #print(unread_notifi)
    context = {
            'directs': directs,
            'active_direct': active_direct,
            'messages': messages,
            'unread_notifi': request.unread_notifi
        }
    return render(request, 'directs/inbox.html', context)
    
@login_required
def directs(request, username):
    user = request.user  #Ibtenemos al usuario logeado
    messages = Message.get_message(user=user) #Obtenemos una lista de "users", "messages" y un contador que devuelve "get_message"
    active_direct = username #Definimos al usuario recipient con el "username" proporcionado por la URL/request.
    recipient = User.objects.get(username=active_direct)
    directs = Message.objects.filter(user=user, reciepient__username=username) #Obtenemos todos los mensajes relacionados principalmente con el usuario actual y con el usuario del recipiente.
    directs.update(is_read=True) #Actualizamos el no leido a leido.
    
    for message in messages:
        if message['user'].username == username or user.username == active_direct: #El request nos envia un username "que hemos seleccionado" y lo compara con el "recepient".
            message['unread'] = 0 #Actualizamos el dato de no leidos a 0.
    
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
    from_user = request.user #Obtenemos al usuario logeado y lo guardamos en "from_user".
    to_user_username = request.POST.get('to_user') #Obtenemos al "remitente/username" que nos envia el form en el campo "to_user".
    body = request.POST.get('body')#Obtenemos al "mensaje" que nos envia el form en el campo "body".
    #print("SendMessage")
    if request.method == "POST": #Tambien, al recibir el form, pasa lo siguiente:
        to_user = User.objects.get(username=to_user_username) #Definimos al campo "to_user/remitente" como obj "User" mediante "to_username"
        Message.send_message(from_user, to_user, body) #Llamamos a la función "send_message" con los campos obtenidos anteriormente.
        redirect_url = reverse('directs:direct', args=[to_user_username]) #Construimos una "URL" con reverse.
        
        context = {
            'unread_notifi': request.unread_notifi    
        }
        return redirect(redirect_url, context) #Y redirigimos a "url direct" que es el chat personal.
    
    else:
        pass #No hagas algo
   
@login_required
def UserSearch(request):
    query = request.GET.get('q')
    context = {'unread_notifi': request.unread_notifi }
    
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        
        #Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
        
        context = {
            'users' : users_paginator,
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