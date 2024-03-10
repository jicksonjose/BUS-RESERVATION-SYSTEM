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
from reservation.models import *

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
def bus_details_list(request, owner_id):
    print(" bus_details_list API HIT")
    try:
 
        bus_details = BusDetails.objects.filter(busowner=owner_id)

        # Serialize the queryset into JSON format
        serializer = BusDetailListSerializer(bus_details, many=True)

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
        bus_details = BusDetails.objects.filter(busowner=owner_id,  is_verified=True)
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
       
        route_id = request.data.get('route')
        print("route id:", route_id)
        date = request.data.get('date')
        print("date:", date)

        route = BusRoute.objects.get(pk=route_id)

        # Create BusSchedule object with retrieved objects
        BusSchedule.objects.create( route=route, date=date)

        # Return success response
        return Response({'message': 'Schedule saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_bus_details(request, owner_id):
    print("API HIT get bus details")
    try:
        # Retrieve bus details for the given owner_id
        bus_details = BusDetails.objects.filter(busowner=owner_id,  is_verified=True)
        bus_details_serializer = BusDetailListSerializer(bus_details, many=True)
        print("bus_details_serializer :", bus_details_serializer)
      
        
        # Combine bus details and routes data into a single response
        data = {
            'bus_details': bus_details_serializer.data,
    
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_bus_route(request):
    print("API HIT save_schedule")
    try:
        # Extract data from request
        bus_id = request.data.get('busname')
        print("bus id:", bus_id)
        start = request.data.get('start')
        print("start :", start)
        destination = request.data.get('destination')
        print("destination:", destination)
        starting_time = request.data.get('starting_time')
        print("starting time:", starting_time)
        destination_time = request.data.get('destination_time')
        print("destination time:", destination_time)


        bus = BusDetails.objects.get(pk=bus_id)
        BusRoute.objects.create(
            bus=bus, 
            start=start, 
            destination=destination, 
            starting_time=starting_time,
            destination_time=destination_time
            )

        #,  Return success response
        return Response({'message': 'Schedule saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return error response if something goes wrong
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def bus_route_list(request, owner_id):
    try:
        # Fetch bus routes for the given owner using a single query
        bus_routes = BusRoute.objects.filter(bus__busowner=owner_id)
        
        # Serialize the queryset of bus routes
        serializer = BusRouteSerializer(bus_routes, many=True)
        
        # Iterate through each serialized bus route and replace bus ID with bus name
        for route_data in serializer.data:
            bus_id = route_data['bus']
            bus_details = BusDetails.objects.get(pk=bus_id)
            route_data['bus'] = bus_details.busname

        # Return the modified serialized data as a JSON response
        print("Bus routes : ", serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus routes"}, status=500)
    

    
@api_view(['GET'])
def bus_schedule_list(request, owner_id):
    print("Api hit")
    try:
        # Convert UUID object to string before filtering
        owner_id_str = str(owner_id)
        
        # Fetch bus schedules for the given owner using a single query
        bus_schedules = BusSchedule.objects.filter(route__bus__busowner_id=owner_id_str)
        
        # Serialize the queryset of bus schedules
        serializer = BusScheduleSerializer(bus_schedules, many=True)
        
        # Return the serialized data as a JSON response
        print("Bus schedules:", serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus schedules"}, status=500)
    

@api_view(['POST'])
def add_bus_point(request):
    print("Bus Point API HIT")
    try:
        route  = request.data.get('busRouteId')
        print("route: ", route)
        stopName = request.data.get('stopName')
        print("stopName: ", stopName)
        stopOrder = request.data.get('stopOrder')
        print("stopOrder: ", stopOrder)
        arrivalTime = request.data.get('arrivalTime')
        print("arrivalTime: ", arrivalTime)
        price = request.data.get('price')
        print("price: ", price)
        
        route_id = BusRoute.objects.get(pk=route)
        BusPoints.objects.create(
            route = route_id,
            stop_name =stopName,
            stop_order = stopOrder,
            arrival_time = arrivalTime,
            price = price,
        )
        return Response({'message': 'Schedule saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['GET'])
def existing_stop_orders(request, route_id, stop_order):
    print("existing_stop_orders API HIT")
    try:
        # Check if there are any existing stop orders for the given route ID and stop order
        existing_orders = BusPoints.objects.filter(route_id=route_id, stop_order=stop_order).exists()
        return Response({"existingOrders": existing_orders})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['GET'])
def bus_points(request, owner_id):
    print("bus_points Api hit")
    try:
        # Convert UUID object to string before filtering
        owner_id_str = str(owner_id)
        
        # Fetch bus schedules for the given owner using a single query
        bus_points = BusPoints.objects.filter( route__bus__busowner_id=owner_id_str)
        # Serialize the queryset of bus schedules
        serializer = ViewBusPointsSerializer(bus_points, many=True)
        
        # Return the serialized data as a JSON response
        print("Bus Points:", serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus schedules"}, status=500)
    


@api_view(['GET'])
def check_schedule_existence(request, route):
    print("check_schedule_existence API HIT")
    try:
        # Check if there are any existing schedules for the given route ID
        existing_schedule = BusSchedule.objects.filter(route=route).exists()
        return Response({"exists": existing_schedule})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['POST'])
def add_bus_staff(request):
    print("Bus add staff API HIT")
    try:
        busowner = request.data.get('busowner_id')
        print("Bus owner  :" + str(busowner))
        first_name  = request.data.get('firstName')
        print("firstName: ", first_name)
        last_name = request.data.get('lastName')
        print("lastName: ", last_name)
        phone = request.data.get('phone')
        print("phone: ", phone)
        type = request.data.get('type')
        print("type: ", type)

   
        bus_staff = BusStaff.objects.create(
            busowner_id=busowner,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            type=type,
        )
        return Response({'message': 'Bus Staff saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['GET'])
def bus_staff_list(request, owner_id):
    print("Api hit")
    try:
        # Convert UUID object to string before filtering
        owner_id_str = str(owner_id)
        
        # Fetch bus schedules for the given owner using a single query
        bus_staff = BusStaff.objects.filter(busowner=owner_id_str)
        
        # Serialize the queryset of bus schedules
        serializer = BusStaffSerializerList(bus_staff, many=True)
        
        # Return the serialized data as a JSON response
        print("Bus Staff:", serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus staff"}, status=500)
    


@api_view(['GET'])
def get_bus_staff(request, owner_id):
    print("API HIT get bus staff")
    try:
        # Retrieve bus staff details for the given owner_id
        bus_staff = BusStaff.objects.filter(busowner=owner_id)
        bus_staff_serializer = BusStaffListSerializer(bus_staff, many=True)
        # Print serialized data for debugging
        print("bus_staff_serializer data:", bus_staff_serializer.data)
    
        # Return the serialized data directly
        return Response(bus_staff_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Return error response with status 500 and error message
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
def get_bus_schedule(request, owner_id):
    print("API HIT get bus schedules")
    try:
        # Retrieve bus schedules for the given owner_id
        bus_schedules = BusSchedule.objects.filter(route__bus__busowner=owner_id)
        bus_schedules_serializer = BusScheduleSerializer(bus_schedules, many=True)
        print("Bus schedules serializer (get) : ", bus_schedules_serializer.data)
        
        return Response(bus_schedules_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def add_bus_staff_schedule(request):
    print("Bus add staff API HIT")
    try:
        staff_id = request.data.get('staff')
        print("Bus staff  :" + staff_id)
        bus_schedule_id  = request.data.get('bus')
        print("bus_schedule: ", bus_schedule_id)
        
        staff = BusStaff.objects.get(id=staff_id)
        print(staff)
        bus_schedule = BusSchedule.objects.get(id=bus_schedule_id)
        print(bus_schedule)
        bus_staff_schedule = BusStaffSchedule.objects.create(
            staff = staff,
            bus_schedule = bus_schedule
        )
        return Response({'message': 'Bus Staff saved successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
    

@api_view(['GET'])
def check_staff_schedule_existence(request, staff_id):
    try:
        # Check if there are any existing bus staff schedules for the given staff ID
        existing_schedules = BusStaffSchedule.objects.filter(staff_id=staff_id).exists()
        print("Found :", existing_schedules)
        return Response({"existing_schedules": existing_schedules}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
@api_view(['GET'])
def bus_staff_schedule_list(request, owner_id):
    try:
        # Fetch bus staff schedules for the given owner_id
        bus_staff_schedules = BusStaffSchedule.objects.filter(staff__busowner_id=owner_id)
        
        # Serialize the queryset of bus staff schedules
        serializer = BusStaffScheduleSerializer(bus_staff_schedules, many=True)
        
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_bus_reservations(request, owner_id):
    print("get bus reservation API HIT")
    try:
        # Filter reservations based on the owner of the bus
        bus_reservations = BusReservation.objects.filter(pickup__route__bus__busowner__id=owner_id)
        print("bus reservation : ", bus_reservations)
        
        # Serialize the queryset
        serializer = BusReservationSerializer(bus_reservations, many=True)
        print("serilzer data :",serializer.data)
        
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

    
@api_view(['GET'])
def get_bus_reservations_bus_details(request, id):
    print("get bus reservation bus details API HIT")
    try:
        # Filter reservations based on the bus ID
        bus_reservations = BusReservation.objects.filter(bus__id=id)
        print("bus reservation bus details: ", bus_reservations)
        
        # Serialize the queryset
        serializer = BusReservationSerializer(bus_reservations, many=True)
        print("serializer data :", serializer.data)
        
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def bus_reservation_route_details(request, route_id):
    print("bus_reservation_route_details API HIT")
    try:
        # Filter reservations based on the route ID
        bus_reservations = BusReservation.objects.filter(pickup__route__id=route_id)
        print(bus_reservations)
        
        # Initialize an empty list to store the combined reservation details
        combined_details = []
        print(combined_details)
        
        for reservation in bus_reservations:
            # Get reservation details for each reservation
            reservation_details = BusReservationDetails.objects.filter(reservation=reservation)
            serialized_reservation_details = BusReservationDetailsSerializer(reservation_details, many=True).data
            
            # Combine reservation and its details
            combined_details.append({
                'reservation': BusReservationSerializer(reservation).data,
                'details': serialized_reservation_details
            })

            # Print the details for debugging
            print(f"Reservation: {reservation}")
            print(f"Reservation Details: {serialized_reservation_details}")
        
        return Response(combined_details)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

    
    
@api_view(['GET'])
def reservation_details(request, id):
    print("reservation_details API HIT")
    try:
        # Filter reservations based on the bus ID
        bus_reservations_id = BusReservation.objects.get(id=id)
        print(bus_reservations_id)
        bus_reservations_details = BusReservationDetails.objects.filter(reservation=bus_reservations_id)
        print("bus reservation bus details: ", bus_reservations_details)
        
        # Serialize the queryset
        serializer = BusReservationDetailsSerializer(bus_reservations_details, many=True)
        print("serializer data :", serializer.data)
        
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

    
    
def check_arrival_time_validity(request, busRouteId, encodedTime):
    print("check_arrival_time_validity API HIT")
    try:
        # Retrieve the bus route with the given ID
        bus_route = BusRoute.objects.get(id=busRouteId)
        print("Bus Rout Id : ",bus_route)

        # Parse the arrival time into hours and minutes
        arrival_hours, arrival_minutes = map(int, encodedTime.split(':'))
        print("arrival_hours : ", arrival_hours, ":",arrival_minutes )

        # Parse the starting time into hours and minutes
        starting_hours, starting_minutes = map(int, bus_route.starting_time.split(':'))
        print("starting time",starting_hours, ":",starting_minutes)

        # Parse the destination time into hours and minutes
        destination_hours, destination_minutes = map(int, bus_route.destination_time.split(':'))
        print('destination_hours :',destination_hours, ":",destination_minutes)

        # Convert everything to minutes for easier comparison
        arrival_total_minutes = arrival_hours * 60 + arrival_minutes
        starting_total_minutes = starting_hours * 60 + starting_minutes
        destination_total_minutes = destination_hours * 60 + destination_minutes

        # Check if the arrival time is within the range
        if starting_total_minutes <= arrival_total_minutes <= destination_total_minutes:
            print("The arrival time is valid")
            print("================================================")
            return JsonResponse({'valid': True})
        else:

            print("Arrival time is not within the range of starting time and destination time.")
            print("================================================")
            return JsonResponse({'valid': False, 'message': 'Arrival time is not within the range of starting time and destination time.'})
    except BusRoute.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Bus route does not exist.'})
    except Exception as e:
        return JsonResponse({'valid': False, 'message': str(e)})
    

def check_arrival_time_validity(request, busRouteId, encodedTime):
    print("check_arrival_time_validity API HIT")
    try:
        # Retrieve the bus route with the given ID
        bus_route = BusRoute.objects.get(id=busRouteId)
        print("Bus Route ID:", bus_route.id)

        # Parse the arrival time into hours and minutes
        arrival_hours, arrival_minutes = map(int, encodedTime.split(':'))
        arrival_total_minutes = arrival_hours * 60 + arrival_minutes

        # Parse the starting time into hours and minutes
        starting_hours, starting_minutes = map(int, bus_route.starting_time.split(':'))
        starting_total_minutes = starting_hours * 60 + starting_minutes

        # Parse the destination time into hours and minutes
        destination_hours, destination_minutes = map(int, bus_route.destination_time.split(':'))
        destination_total_minutes = destination_hours * 60 + destination_minutes

        # Check if the arrival time is within the range of starting time and destination time
        if starting_total_minutes <= arrival_total_minutes <= destination_total_minutes:
            print("The arrival time is within the range of starting time and destination time.")

            # Get the latest arrival time of bus points for the route
            latest_arrival_time = BusPoints.objects.filter(route=bus_route).latest('arrival_time').arrival_time

            # Parse the latest arrival time into hours and minutes
            latest_arrival_hours, latest_arrival_minutes = map(int, latest_arrival_time.split(':'))
            latest_arrival_total_minutes = latest_arrival_hours * 60 + latest_arrival_minutes

            # Check if the arrival time is greater than the latest stop order arrival time
            if arrival_total_minutes > latest_arrival_total_minutes:
                print("The arrival time is valid.")
                return JsonResponse({'valid': True})
            else:
                print("Arrival time is not greater than the latest stop order arrival time.")
                return JsonResponse({'valid': False, 'message': 'Arrival time must be greater than the latest stop order arrival time.'})
        else:
            print("Arrival time is not within the range of starting time and destination time.")
            return JsonResponse({'valid': False, 'message': 'Arrival time is not within the range of starting time and destination time.'})

    except BusRoute.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Bus route does not exist.'})
    except BusPoints.DoesNotExist:
        print("No bus points exist for the route.")
        return JsonResponse({'valid': True})  # No bus points exist, so arrival time is valid
    except Exception as e:
        return JsonResponse({'valid': False, 'message': str(e)})
