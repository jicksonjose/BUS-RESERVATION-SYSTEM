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
from rest_framework import status


@api_view(['POST'])
def add_bus_details(request):
    print("API HIT")
    if request.method == 'POST':
        try:
            # Create serializer instance with request data
            serializer = BusDetailSerializer(data=request.data)

            if serializer.is_valid():
                # Save the validated data
                serializer.save()
                return JsonResponse({"status": "success", "message": "Bus details added successfully"})
            else:
                print("Serializer errors:", serializer.errors)
                return JsonResponse({"status": "error", "message": "Invalid data", "errors": serializer.errors}, status=400)

        except BusOwner.DoesNotExist:
            return JsonResponse({"status": "error", "message": "BusOwner does not exist"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@api_view(['GET'])
def bus_details_list(request):
    print("API HIT")
    try:
        # Get all bus details from the database
        bus_list = BusDetails.objects.all()

        # Serialize the queryset into JSON format
        serializer = BusDetailListSerializer(bus_list, many=True)

        # Return the serialized data as a JSON response
        print("Bus list :" , serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus details"}, status=500)



@api_view(['GET'])
def get_bus_details_and_routes(request, owner_id):
    try:
        # Retrieve bus details for the given owner_id
        bus_details = BusDetails.objects.filter(busowner=owner_id)
        bus_details_serializer = BusDetailListSerializer(bus_details, many=True)
        print("bus_details_serializer :", bus_details_serializer)
      
        bus_routes = BusRoute.objects.filter(bus__in=bus_details)
        bus_routes_serializer = BusRouteSerializer(bus_routes, many=True)
        print("bus_routes_serializer :", bus_routes_serializer)
        
        # Combine bus details and routes data into a single response
        data = {
            'bus_details': bus_details_serializer.data,
            'bus_routes': bus_routes_serializer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_schedule(request):
    print("API HIT save_schedule")
    try:
        # Extract data from request
        bus_id = request.data.get('busname')
        print("bus id:", bus_id)
        route_id = request.data.get('route')
        print("route id:", route_id)
        date = request.data.get('date')
        print("date:", date)

        # Retrieve BusDetails and BusRoute objects using their IDs
        bus = BusDetails.objects.get(pk=bus_id)
        route = BusRoute.objects.get(pk=route_id)

        # Create BusSchedule object with retrieved objects
        BusSchedule.objects.create(bus=bus, route=route, date=date)

        # Return success response
        return Response({'message': 'Schedule saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
