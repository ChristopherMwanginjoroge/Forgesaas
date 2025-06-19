from django.urls import path,re_path
from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    OtpVerificationView,
    OtpResendview
)



urlpatterns = [
        re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
  
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

    path('otp/verify/', OtpVerificationView.as_view(), name='otp-verify'), 
    path('otp/resend/', OtpResendview.as_view(), name='otp-resend'),  
]