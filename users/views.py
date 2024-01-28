from imaplib import _Authenticator
from users.models import *
from rest_framework.decorators import api_view
from . serializer import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F, Value, IntegerField
from django.db import transaction
import traceback
from django.db.models import Case, When, Value, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.http import JsonResponse





    
@csrf_exempt
@api_view(["POST"])
def signup(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            print("Received data:", received_data)

            # Check if the email already exists
            if BusOwner.objects.filter(email=received_data['email']).exists():
                print("Email already exists")
                return JsonResponse({"status": "error", "message": "Email already exists"}, status=400)

            # Check if the phone number already exists
            if BusOwner.objects.filter(phone=received_data['phone']).exists():
                print("Phone number already exists")
                return JsonResponse({"status": "error", "message": "Phone number already exists"}, status=400)

            serializer = BusOwnerSignupSerializers(data=received_data)
            print("Serialized data:", serializer)

            if serializer.is_valid():
                serializer.save()
                print("Account added successfully")
                return JsonResponse({"status": "added"})
            else:
                print("Serializer errors:", serializer.errors)
                return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)

        except json.JSONDecodeError as e:
            print("Invalid JSON format in request body")
            return JsonResponse({"status": "error", "message": "Invalid JSON format in request body"}, status=400)

    print("Invalid request method")
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@api_view(['GET'])
def get_email(request, email):
    try:
        print("API Endpoint Hit!")
        check_email = BusOwner.objects.filter(email=email).exists()
        response_data = {'exists': check_email}
        print("check_email:", response_data)
        return JsonResponse(response_data)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

def check_phone(request, phone):
    try:
        # Convert the phone parameter to an integer (assuming it's a numeric phone number)
        phone = int(phone)
    except ValueError:
        return JsonResponse({"exists": False, "message": "Invalid phone number format"})

    # Your logic to check if the phone number exists
    # Example: You can use BusOwner.objects.filter(phone=phone).exists()
    phone_exists = BusOwner.objects.filter(phone=phone).exists()

    # Return a JSON response indicating whether the phone number exists
    return JsonResponse({"exists": phone_exists})


@csrf_exempt
def login(request):
    if request.method == 'POST':

        receieved_data = json.loads(request.body)
        print(receieved_data)
        getemail = receieved_data["email"]
        getpassword = receieved_data["password"]
        data = list(BusOwner.objects.filter(Q(email__exact=getemail) & Q(password__exact=getpassword)).values())
        return HttpResponse(json.dumps(data)) 
    else:
        return HttpResponse(json.dumps({"status": "login details Invalid"}))  
