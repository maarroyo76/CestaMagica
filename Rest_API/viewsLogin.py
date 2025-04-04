from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

@csrf_exempt
@api_view(['POST'])
def Login(request):
    data = JSONParser().parse(request)

    username = data['username']
    password = data['password']

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response('Usuario no válido', status=status.HTTP_400_BAD_REQUEST)
    
    pass_valido = check_password(password, user.password)

    if not pass_valido:
        return Response('Contraseña incorrecta', status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    return Response(token.key, status=status.HTTP_200_OK)
