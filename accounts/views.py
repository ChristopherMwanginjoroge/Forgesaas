from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OtpVerificationSerializer,OtpResendSerializer
from django.contrib.auth import get_user_model
from .models import Otp
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from datetime import timezone
import random
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



class OtpVerificationView(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self,request,*args,**kwargs):
        serializer=OtpVerificationSerializer(data=request.data)


        if serializer.is_valid():
            otp_code=serializer.validated_data['otp_code']
            otp_token=serializer.validated_data['otp_token']

            try:
                otp=Otp.objects.get(token=otp_token)
            except Otp.DoesNotExist:
                return Response({'detail':"Invalid or expired otp token"},status=status.HTTP_400_BAD_REQUEST)
            
            if otp.otp_code != otp_code:
                return Response({"deatil":"invaid otp code"},status=status.HTTP_400_BAD_REQUEST)
            
            if otp.is_expired():
                return Response({"detail":"Otp has expired , please request a new one"},status=status.HTTP_400_BAD_REQUEST)
            
            user=otp.user
            user.is_active=True
            user.save()

            refresh=RefreshToken.for_user(user)
            access_token=str(refresh.access_token)
            refresh_token=str(refresh)

            response= Response({
                'detail':"Email verified successfully",
                'access':access_token,
                'refresh':refresh_token

            })

            response.set_cookie(
                'access',access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
          
            response.set_cookie(
                'refresh',refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH__COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE

            )
            return response
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class OtpResendview(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self,request,*args,**kwargs):
        serializer=OtpResendSerializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']


            try:
                user=get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                return Response({"detail":"user does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_active:
                return Response({"detail":"user is already active"},status=status.HTTP_400_BAD_REQUEST)
            
            otp_code=''.join([str(random.randint(0,9))for _ in range(6)])
            otp_token=Otp.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=timezone.now()+timezone.timedelta(minutes=5)
            )
            subject = "Your OTP for Email Verification"
            message = f"Hi {user.user_name},\n\nYour OTP is {otp_code}. It will expire in 5 minutes.\n\nBest,\nTeam"
            send_mail(subject, message, 'learnerviner@gmail.com', [user.email])

            return Response({"detail","A new otp code has been sent to your email:"},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class CustomProviderAuthView(ProviderAuthView):
    def post(self,request,*args,**kwargs):
        response=super().post(request,*args,**kwargs)

        if response.status.code == 201:
            access_token=response.data.get('access')
            refresh_token=response.data.get('refresh')

            response.set_cookie(
                'access',access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
          
            response.set_cookie(
                'refresh',refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH__COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE

            )
            
        return response
    
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self,request,*args,**kwargs):
        response=super().post(request,*args,**kwargs)

        if response.status_code == 200:
            access_token=response.data.get('access')
            refresh_token=response.data.get('refresh')

            response.set_cookie(
                'access',access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
          
            response.set_cookie(
                'refresh',refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH__COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE

            )
            
        return response
    

class CustomTokenRefreshView(TokenRefreshView):
    def post(self,request,*args,**kwargs):
        refresh_token=request.cookies.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token


        response=super().post(request,*args,**kwargs)


        if response.status_code == 200:
            access_token=response.data.get('access')

            response.set_cookie(
                'access',access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
          
            response.set_cookie(
                'refresh',refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH__COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE

            )

        return response
    
class CustomTokenVerifyView(TokenVerifyView):
    def post(self,request,*args,**kwargs):
        access_token=request.cookies.get('access')

        if access_token:
            request.data['token']='access_token'

        return super().post(request,*args,**kwargs)
    



    



        



        

            


    



        

