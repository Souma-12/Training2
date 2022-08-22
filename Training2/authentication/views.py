from ast import Expression
from tokenize import Token
from django.shortcuts import render
from rest_framework import response , status, permissions, generics, views
from rest_framework.generics import GenericAPIView
from authentication import serializers
from authentication.serializers import  RegisterSerializer,LoginSerializer,LogoutSerializer
from authentication.serializers import  EmailVerificationSerialzer,ResetPasswordEmailRequestSerialializer,SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.encoding import smart_str, force_str,smart_bytes,DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.response import Response






class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegisterSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email = user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink=reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink +"?token="+str(token)
            email_body = 'Hi' +user.username+ 'Use link below to verify your email \n' + absurl
            data = {'email_body':email_body,'to_email':user.email, 'email_subject': 'Verify your email'}
            Util.send_email(data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerialzer
    token_param_config= openapi.Parameter('token', in_=openapi.IN_QUERY, description= 'Description',type= openapi.TYPE_STRING)
   
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        print("*********",request)
        token = request.query_params['token']
        print("*********1",token)
        try:
            payload=jwt.decode(token,settings.SECRET_KEY, algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response({'email':'Successfully activated'}, status= status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
                 return response.Response({'error':'Activation Expired'}, status= status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
                 return response.Response({'error':'Invalid token'}, status= status.HTTP_400_BAD_REQUEST)
                


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)




class RequestPasswordResetEmail(generics.GenericAPIView):
    # authentication_classes= []
    serializer_class = ResetPasswordEmailRequestSerialializer
    def post(self, request):
        serializers=self.serializer_class(data=request)
        email = request.data['email']
        if User.objects.filter(email = email).exists():
                user = User.objects.get(email= email)
                uidb64 =urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink=reverse('password-reset-confirm',kwargs={'uidb64': uidb64, 'token':token})
                redirect_url=request.data.get('redirect_url', '')
                absurl = 'http://'+current_site + relativeLink 
                email_body = 'Hello,\n Use link below to reset your password \n' + absurl 
                data = {'email_body':email_body,'to_email':user.email, 'email_subject': 'Reset your password'}
                Util.send_email(data)
   
        return response.Response({ 'success': 'we have sent you a link to reset your password'},status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerialializer
    def get(self, request, uidb64, token):

        # redirect_url=request.Get.get('redirect_url')
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            

            if not PasswordResetTokenGenerator().check_token(user,token):
                return response.Response({ 'error': 'Token is not valid,please request a new one'},status=status.HTTP_401_UNAUTHORIZED)

            return response.Response({'success': True,'message': 'Credentials Valid', 'uidb64': uidb64,'token':token, },status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:

            if PasswordResetTokenGenerator().check_token(user):
                return response.Response ({'error': 'Token is not valid,please request a new one'},status=status.HTTP_401_UNAUTHORIZED)

class SetNePasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)  
        return response.Response({'success': True,'message': 'Password reset success' },status=status.HTTP_200_OK)     