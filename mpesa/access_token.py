import requests
from django.http import JsonResponse
from django.conf import settings
from requests.auth import HTTPBasicAuth

def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = r.json().get('access_token')
    return access_token


    


