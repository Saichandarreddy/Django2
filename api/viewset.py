from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib import auth#.auth import authenticate,login,logout
from rest_framework import status
from rest_framework.response import Response
import django
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@permission_classes((IsAuthenticated, ))
@api_view(['post'])
def login(request):
    try:
        rd = request.data
        print(request)
        user = auth.authenticate(username=rd['username'],password=rd['password'])
        if user is not None:
            auth.login(request, user)
            if not request.session.session_key:
                session = request.session.create()
            else:
                session = request.session.session_key
                request.session.set_expiry(60*30)
            resp={}
            resp["session_key"] = request.session
            resp["csrf"]= django.middleware.csrf.get_token(request)
            resp['message']='Login Successful'
            return Response(resp,status=status.HTTP_200_OK)
        else:
            return Response({'error':{'code':5000,'message':'Incorrect username/password'}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)

@api_view(['get'])
def logout(request):
    try:
        auth.logout(request)
        response = HttpResponse()
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return Response({'message':'Success'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
