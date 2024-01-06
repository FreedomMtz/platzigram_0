"""platzigram views."""
#Django
from django.http import HttpResponse, JsonResponse

#Utilites (funciones que no son de django)
from datetime import datetime



###definimos una funcion llamada 'hello_world' 
def hello_world(request):
    """Definimos un elemento para guardar la fecha actual."""
    now= datetime.now().strftime('%dth, %b, %Y -%H:%M hrs')
    """Aqui retornamos el mensaje de hello world."""
    return HttpResponse("Oh, hi! Current server time is {now}".format(now=now))

def sort_integers(request):
    """Return a JSON respons with sorted integers ."""
    """ import pdb; pdb.set_trace() """ #ejecuta una consola para interactuar con "request"
    numbers = request.GET['numbers'] #obtenemos la lista de los numero ingresados con el diccionario "?numbers"
    list_numbers = list(map(int, numbers.split(','))) 
    sorted_numbers = sorted(list_numbers)
    data = {
        'status' : 'Ok',
        'number': sorted_numbers,
        'message' : 'Integers sorted sucsessfuly.'
    }
    """ return HttpResponse(str(sorted_numbers)) """
    return JsonResponse(data)

def say_hi(request, name, age):
    """say_hi recibe "request" "name" y "age" que son los datos que recive de las peticiones """
    if age < 12:
        message = 'Sorry {user_name}, your are not allowed here'.format(user_name=name)
    else :
        message = 'Hello, {user_name}! Welcome to Platzigram'.format(user_name=name)
    
    return HttpResponse(message)