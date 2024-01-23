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




    
@csrf_exempt
@api_view(["POST"])
def signup(request):
    try:
        transaction.set_autocommit(False)
        serialized = SignupSerializers(data=request.data)
        if serialized.is_valid():
            name = request.data["name"]
            email = request.data["email"]
            phone = request.data["phone"]
            password = request.data["password"]
            if BusOwner.objects.filter(email=email).exists():
                response_data={
                    "StatusCode":6001,
                    "data":"email already exists"
                }
            elif BusOwner.objects.filter(phone=phone).exists():
                response_data = {
                    "StatusCode": 6001,
                    "data": "Phone number already exists"
                }
            else:  
                owner= BusOwner.objects.create(
                    name = name,
                    email = email,
                    phone = phone,
                    password = password,
                ) 
                transaction.commit()
                response_data = {
                    "StatusCode":6000,
                    "data":{
                        "message":f"{owner.name} created succesfully"
                    }
                }         
        else:
            response_data = {
                    "StatusCode": 6001,
                    "data": serialized._errors
                }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }
    return Response({'app_data': response_data}, status=status.HTTP_200_OK)



@api_view(["POST"])
def login(request):
    try:
        transaction.set_autocommit(False)
        serializer = LoginSerializers(data=request.data)

        if serializer.is_valid():
            email = request.data["email"]
            password = request.data["password"]

            user = BusOwner.objects.filter(email=email, password=password).first()

            if user is not None:
                # User is authenticated, you can add additional logic here if needed
                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "message": "Login successful",
                        "user_id": user.id  # You can customize the response based on your needs
                    }
                }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "message": "Invalid credentials"
                    }
                }
        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "message": "Invalid credentials"
                }
            }

    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    # Return the response after the try-except block
    return Response({'app_data': response_data}, status=status.HTTP_200_OK)