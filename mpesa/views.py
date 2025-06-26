from django.shortcuts import render
import datetime
from django.conf import settings
from django.http import JsonResponse
from .access_token import get_access_token
import requests
import base64
import json
from django.views.decorators.csrf import csrf_exempt

def lipa_na_mpesa_online(request):
    access_token = get_access_token()
    api_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1000,
        "PartyA": "25412337361",  # User's phone number
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": "254116969025",  # Same as PartyA
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "HA",
        "TransactionDesc": f"Payment for order  on MJENGO PLUg"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return JsonResponse(response.json())


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    print("Callback Data:", data)
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})




