from django.urls import path
from . import views

urlpatterns = [
    path('stk-push/', views.lipa_na_mpesa_online, name='stk-push'),
    path('callback/', views.mpesa_callback, name='mpesa-callback'),
]