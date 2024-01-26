from django.shortcuts import render
from . models import *
from . serializer import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse


@csrf_exempt
def add_bus_document(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            print(received_data)
            serialized_data = BusDocumentSerializer(data=received_data)
            print("serailized data :", serialized_data)

            if serialized_data.is_valid():
                serialized_data.save()
                return HttpResponse({"status": "added"})
            else:
                return HttpResponse({"status": "error", "errors": serialized_data.errors}, status=400)

        except BusOwner.DoesNotExist:
            return HttpResponse({"status": "error", "message": "BusOwner does not exist"}, status=400)

    return HttpResponse({"status": "error", "message": "Invalid request method"}, status=400)



@csrf_exempt
def add_bus_details(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            print("received_data:", received_data)

            # Fetch BusNumber instance based on bus number
            busnumber_str = received_data.get('busnumber', '')
            try:
                busnumber_instance = BusNumber.objects.get(busnumber=busnumber_str)
                received_data['busnumber'] = busnumber_instance.pk
            except BusNumber.DoesNotExist:
                return JsonResponse({"status": "error", "message": f"BusNumber '{busnumber_str}' does not exist"}, status=400)

            # Deserialize the data
            serializer = BusDetailsSerializer(data=received_data)
            print("serialized data:", serializer)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "added"})
            else:
                print("Serializer errors:", serializer.errors)
                return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({"status": "error", "message": "Invalid JSON format in request body"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@api_view(['GET'])
def get_bus_numbers(request, busowner):
    try:
        print("API Endpoint Hit!")
        bus_numbers = BusNumber.objects.filter(busowner=busowner).values_list('busnumber', flat=True)
        response_data = {'busnumbers': list(bus_numbers)}
        print("bus numbers:", response_data)
        return JsonResponse(response_data)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)