from authentication import views
from django.urls import path,include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenRefreshView,)
from .views import LoginAPIView, RegisterAPIView, RequestPasswordResetEmail, SetNePasswordAPIView, LogoutAPIView,VerifyEmail,PasswordTokenCheckAPI






urlpatterns = [
    
    path('register/',RegisterAPIView.as_view(), name="register"),
    path('email-verify/',VerifyEmail.as_view(), name="email-verify"),
    path('login/',LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path('password-reset-complete/',SetNePasswordAPIView.as_view(), name="password-reset-complete"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),




]