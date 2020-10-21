from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from django.contrib.auth.base_user import BaseUserManager

import requests

from .serializers import UserSerializer, UserLoginHistorySerializer, GoogleLoginSerializer
from .models import User
from .utils import get_google_client_id


def save_and_send_login(data):
    url = 'https://www.w3schools.com/python/demopage.php'
    result = request.post(url, data=data)

    serializer = UserLoginHistorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()

class UserViewSet(ViewSet):
    serializer_class = UserSerializer
    
    def create(self, request):
        res = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            res['message'] = 'User signed up successfully, please Login to continue!'
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res['message'] = 'Failed to sign up user!'
            res['errors']  =  serializer.errors
            print('error_messages', serializer.error_messages)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        res = {}
        data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data['username'])
            data['user'] = user.pk
            data['ip']   = request.META['REMOTE_ADDR']
            save_and_send_login(data)
            
            res['message'] = 'User successfully logged in!'
            res['tokens']  = serializer.validated_data
            return Response(res, status=status.HTTP_202_ACCEPTED)

        else:
            res['message'] = 'Falided to login user!'
            res['errors']  = serializer.errors
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginViewSet(ViewSet):

    def create(self, request):
        res = {}
        data = {}
        jwt_token = {}
        token = request.data['token']
        client_id = get_google_client_id()
        try:
            user_info = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
            user, created = User.objects.get_or_create(username=user_info['email'])
            if created:
                user.set_password(BaseUserManager().make_random_password())
                user.save()

            data['user'] = user.pk
            data['ip']   = request.META['REMOTE_ADDR']
            save_and_send_login(data)

            tokens = RefreshToken.for_user(user)
            jwt_token['access']  = str(tokens.access_token)
            jwt_token['refresh'] = str(tokens)
            res['message'] = 'User successfully logged in using Google!'
            res['tokens']  = jwt_token
            return Response(res, status=status.HTTP_202_ACCEPTED)

        except ValueError:
            res['message'] = 'Failed to login user using Google!'
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
