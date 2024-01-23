from users.models import *
from rest_framework.decorators import api_view
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.http import HttpResponse

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        receieved_data = json.loads(request.body)
        print(receieved_data)
        serialized_data  = SignupSerializers(data=receieved_data)
        if serialized_data.is_valid():
            serialized_data.save()
            return HttpResponse(json.dumps({"status": "Registered successfully"}))    
        else:
            return HttpResponse(json.dumps({"status": "error"}))   

@csrf_exempt
def loginApi(request):
    if request.method == 'POST':
        receieved_data = json.loads(request.body)
        print(receieved_data)
        getemail = receieved_data["email"]
        getpassword = receieved_data["password"]
        data = list(BusOwner.objects.filter(Q(email__exact=getemail) & Q(password__exact=getpassword)).values())
        return HttpResponse(json.dumps(data)) 
    else:
        return HttpResponse(json.dumps({"status": "login details Invalid"})) 