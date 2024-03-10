from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from users.models import *
from rest_framework.decorators import api_view

# from users.se import send_otp_to_email
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
import random
from reservation.models import *
from django.core.mail import send_mail
import uuid
from django.conf import settings

@csrf_exempt
# @api_view(["POST"])
# def signup(request):
#     if request.method == 'POST':
#         try:
#             received_data = json.loads(request.body)
#             print("Received data:", received_data)

#             # Check if the email already exists
#             if BusOwner.objects.filter(email=received_data['email']).exists():
#                 print("Email already exists")
#                 return JsonResponse({"status": "error", "message": "Email already exists"}, status=400)

#             # Check if the phone number already exists
#             if BusOwner.objects.filter(phone=received_data['phone']).exists():
#                 print("Phone number already exists")
#                 return JsonResponse({"status": "error", "message": "Phone number already exists"}, status=400)

#             serializer = BusOwnerSignupSerializers(data=received_data)
#             print("Serialized data:", serializer)

#             if serializer.is_valid():
#                 serializer.save()
#                 print("Account added successfully")
#                 return JsonResponse({"status": "added"})
#             else:
#                 print("Serializer errors:", serializer.errors)
#                 return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)

#         except json.JSONDecodeError as e:
#             print("Invalid JSON format in request body")
#             return JsonResponse({"status": "error", "message": "Invalid JSON format in request body"}, status=400)

#     print("Invalid request method")
#     return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def send_otp_to_email(email, otp_code):
    subject = 'Your OTP for Signup'
    message = f'Your OTP for signup is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return True


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

            generated_otp = ''.join(random.choice('0123456789') for i in range(6))
            received_data['otp'] = generated_otp
            

            serializer = BusOwnerSignupSerializers(data=received_data)
            send_otp_to_email(received_data['email'], generated_otp)

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
    



@api_view(['POST'])
def verify_otp(request):
    print("API HIT")
    
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body.decode('utf-8'))
            otp = int(received_data.get('otp'))
            name = received_data.get('name', '')  
            email = received_data.get('email', '')  
            phone = received_data.get('phone', '')  
            password = received_data.get('password', '')  

            print("name:", name)
            print("email:", email)
            print("phone:", phone)
            print("password:", password)

            # Check if the OTP exists in the database
            with transaction.atomic():
                otp_object = Otp.objects.select_for_update().filter(otp=otp, email=email).first()

                if otp_object:
                    # Check if the OTP is expired
                    if otp_object.is_expired:
                        response_data = {'status': 'expired'}
                    else:
                        # Check if the OTP is verified
                        if otp_object.is_verified:
                            response_data = {'status': 'already_verified'}
                        else:
                            # Check if the OTP is invalid
                            if not otp_object.is_valid():
                                # Increase the attempt count only for invalid attempts
                                otp_object.attempt += 1
                                otp_object.save()

                                # Check if the attempt limit has been reached (e.g., 5 attempts)
                                if otp_object.attempt >= 5:
                                    otp_object.is_expired = True  # Mark OTP as expired
                                    otp_object.save()
                                    response_data = {'status': 'attempt_limit_exceeded'}
                                else:
                                    response_data = {'status': 'invalid'}
                            else:
                                # Set the OTP status to 'verified'
                                otp_object.is_verified = True
                                otp_object.save()

                                # Save details to bus owner model
                                bus_owner = BusOwner(name=name, email=email, phone=phone, password=password)
                                bus_owner.save()

                                response_data = {'status': 'verified', 'name': name, 'email': email, 'phone': phone, 'password': password}
                else:
                    response_data = {'status': 'invalid'}

            print("Response data:", response_data)
            return JsonResponse(response_data)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



#================ User side ===================

    
@api_view(['GET'])
def bus_search_list(request):
    print("bus_search_list Api hit")
    try:

        bus_details = BusDetails.objects.filter(is_verified=True)
        
        # Serialize the queryset of bus schedules
        serializer = SearchBusDetailListSerializer(bus_details, many=True)
        
        # Return the serialized data as a JSON response
        print("Bus Details:", serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus schedules"}, status=500)
    
@api_view(['GET'])
def bus_stop_name(request):
    print("bus_stop_name Api hit")
    try:
        stop_name = BusPoints.objects.all()  # Corrected line
        
        # Serialize the queryset of bus stop names
        serializer = BusPointsStopNameSerializer(stop_name, many=True)
        
        # Return the serialized data as a JSON response
        print("Bus Stop Names:", serializer.data)
        return Response(serializer.data)

    except Exception as e:
        print("Error:", e)
        return Response({"status": "error", "message": "An error occurred while fetching bus stop names"}, status=500)

# def search_buses(request):
#     if request.method == 'GET':
#         from_stop = request.GET.get('from', '')
#         to_stop = request.GET.get('to', '')
#         date = request.GET.get('date', '')

#         print("from_stop:", from_stop)
#         print("to_stop:", to_stop)
#         print("date:", date)

#         try:
#             from_route_ids = BusPoints.objects.filter(stop_name=from_stop).values_list('route_id', flat=True)
#             print("from_route_ids:", from_route_ids)
#             to_route_ids = BusPoints.objects.filter(stop_name=to_stop).values_list('route_id', flat=True)
#             print("to_route_ids:", to_route_ids)
#             common_route_ids = set(from_route_ids).intersection(to_route_ids)
#             print("common_route_ids:", common_route_ids)

#             if not common_route_ids:
#                 print("No buses found for the given stops.")
#                 return JsonResponse({'error': 'No buses found for the given stops.'})

#             valid_buses = []
#             for bus_id in common_route_ids:
#                 # Get the bus points for the current route ID
#                 bus_points = BusPoints.objects.filter(route_id=bus_id, stop_name__in=[from_stop, to_stop]).order_by('stop_order')
#                 if len(bus_points) != 2:
#                     # Skip this route if either the start or destination stop is not found
#                     continue

#                 # Extract bus point IDs
#                 from_bus_point_id = bus_points[0].id
#                 to_bus_point_id = bus_points[1].id

#                 # Fetch bus schedule for the current route ID
#                 bus_schedule = BusSchedule.objects.filter(route_id=bus_id, status=BusSchedule.ACTIVE).first()
#                 if bus_schedule:
#                     route_id = bus_schedule.route.id
#                     bus_route = str(bus_schedule.route)
#                     start = bus_schedule.route.start
#                     destination = bus_schedule.route.destination
#                     starting_time = bus_schedule.route.starting_time
#                     destination_time = bus_schedule.route.destination_time
#                     bus_details = bus_schedule.route.bus  # Fetch related BusDetails instance

#                     bus_details_data = {
#                         'bus_id': bus_details.id,
#                         'busname': bus_details.busname,
#                         'busrc': bus_details.busrc.url if bus_details.busrc else None,  # Get URL of busrc field if exists
#                         'registration_number': bus_details.registration_number,
#                         'thumbnail': bus_details.thumbnail.url if bus_details.thumbnail else None,  # Get URL of thumbnail field if exists
#                         'ac_nonac': bus_details.ac_nonac,
#                         'wifi': bus_details.wifi,
#                         'food': bus_details.food,
#                         'drink': bus_details.drink,
#                         'is_verified': bus_details.is_verified,
#                     }

#                     result = {
#                         'route_id': route_id,
#                         'bus_route': bus_route,
#                         'from_stop': from_stop,
#                         'to_stop': to_stop,
#                         'date': date,
#                         'start': start,
#                         'destination': destination,
#                         'starting_time': starting_time,
#                         'destination_time': destination_time,
#                         'bus_details': bus_details_data,
#                         'from_bus_point_id': from_bus_point_id,
#                         'to_bus_point_id': to_bus_point_id,
#                     }

#                     print("Result:", result)
#                     valid_buses.append(result)

#             if not valid_buses:
#                 print("No valid buses found for the given stops.")
#                 return JsonResponse({'error': 'No valid buses found for the given stops.'})

#             return JsonResponse(valid_buses, safe=False)

#         except Exception as e:
#             print("Error:", e)
#             return JsonResponse({'error': 'An internal server error occurred.'}, status=500)

        
def search_buses(request):
    if request.method == 'GET':
        from_stop = request.GET.get('from', '')
        to_stop = request.GET.get('to', '')
        date = request.GET.get('date', '')

        print("from_stop:", from_stop)
        print("to_stop:", to_stop)
        print("date:", date)

        try:
            # Get the stop order for the from and to stops
            from_stop_order = BusPoints.objects.filter(stop_name=from_stop).first().stop_order
            to_stop_order = BusPoints.objects.filter(stop_name=to_stop).first().stop_order

            # Ensure that from_stop_order is less than to_stop_order
            if from_stop_order >= to_stop_order:
                return JsonResponse({'error': 'From stop must be before the to stop.'})

            from_route_ids = BusPoints.objects.filter(stop_name=from_stop).values_list('route_id', flat=True)
            print("from_route_ids:", from_route_ids)
            to_route_ids = BusPoints.objects.filter(stop_name=to_stop).values_list('route_id', flat=True)
            print("to_route_ids:", to_route_ids)
            common_route_ids = set(from_route_ids).intersection(to_route_ids)
            print("common_route_ids:", common_route_ids)

            if not common_route_ids:
                print("No buses found for the given stops.")
                return JsonResponse({'error': 'No buses found for the given stops.'})

            valid_buses = []
            for bus_id in common_route_ids:
                # Get the bus points for the current route ID
                bus_points = BusPoints.objects.filter(route_id=bus_id, stop_name__in=[from_stop, to_stop]).order_by('stop_order')
                if len(bus_points) != 2:
                    # Skip this route if either the start or destination stop is not found
                    continue

                from_bus_point = bus_points[0]
                to_bus_point = bus_points[1]

                # Print details of the from and to bus points fields
                print("From Bus Point Details:")
                print("========================")
                print("Stop Name:", from_bus_point.stop_name)
                print("Stop Order:", from_bus_point.stop_order)
                print("Arrival Time:", from_bus_point.arrival_time)  # Include arrival time here
                print("Price:", from_bus_point.price)
                print("========================")
                print("To Bus Point Details:")
                print("========================")
                print("Stop Name:", to_bus_point.stop_name)
                print("Stop Order:", to_bus_point.stop_order)
                print("Arrival Time:", to_bus_point.arrival_time)  # Include arrival time here
                print("Price:", to_bus_point.price)
                print("========================")

                # Extract bus point IDs
                from_bus_point_id = from_bus_point.id
                to_bus_point_id = to_bus_point.id

                # Fetch bus schedule for the current route ID
                bus_schedule = BusSchedule.objects.filter(route_id=bus_id, status=BusSchedule.ACTIVE).first()
                if bus_schedule:
                    route_id = bus_schedule.route.id
                    bus_route = str(bus_schedule.route)
                    start = bus_schedule.route.start
                    destination = bus_schedule.route.destination
                    starting_time = bus_schedule.route.starting_time
                    destination_time = bus_schedule.route.destination_time
                    bus_details = bus_schedule.route.bus  # Fetch related BusDetails instance

                    bus_details_data = {
                        'bus_id': bus_details.id,
                        'busname': bus_details.busname,
                        'busrc': bus_details.busrc.url if bus_details.busrc else None,  # Get URL of busrc field if exists
                        'registration_number': bus_details.registration_number,
                        'thumbnail': bus_details.thumbnail.url if bus_details.thumbnail else None,  # Get URL of thumbnail field if exists
                        'ac_nonac': bus_details.ac_nonac,
                        'wifi': bus_details.wifi,
                        'food': bus_details.food,
                        'drink': bus_details.drink,
                        'is_verified': bus_details.is_verified,
                    }

                    result = {
                        'route_id': route_id,
                        'bus_route': bus_route,
                        'from_stop': from_stop,
                        'to_stop': to_stop,
                        'date': date,
                        'start': start,
                        'destination': destination,
                        'starting_time': starting_time,
                        'destination_time': destination_time,
                        'bus_details': bus_details_data,
                        'from_bus_point_id': from_bus_point_id,
                        'to_bus_point_id': to_bus_point_id,
                        'from_arrival_time': from_bus_point.arrival_time,
                        "to_arrival_time": to_bus_point.arrival_time
                        
                    }

                    print("Result:", result)
                    valid_buses.append(result)

            if not valid_buses:
                print("No valid buses found for the given stops.")
                return JsonResponse({'error': 'No valid buses found for the given stops.'})

            return JsonResponse(valid_buses, safe=False)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': 'An internal server error occurred.'}, status=500)

        
def bus_book_seat(request, bus_id, route_id, from_bus_point_id, to_bus_point_id):
    print("bus_book_seat API HIT")
    try:
        # Retrieve the bus details using the provided bus_id
        bus_details = BusDetails.objects.get(id=bus_id)
        
        # Retrieve the bus route details using the provided route_id
        bus_route = BusRoute.objects.get(id=route_id)

        # Retrieve the bus point details using the provided from_bus_point_id and to_bus_point_id
        from_bus_point = BusPoints.objects.get(id=from_bus_point_id)
        print("form bus point details :", from_bus_point)
        to_bus_point = BusPoints.objects.get(id=to_bus_point_id)
        print("To bus point details :", to_bus_point)

        # Calculate the total price (for demonstration, you can replace it with your actual calculation logic)
        total_price = from_bus_point.price + to_bus_point.price

        # Serialize the bus details, bus route details, and total price to JSON
        bus_details_json = {
            'bus_id':bus_details.id,
            'busname': bus_details.busname,
            'busrc': bus_details.busrc.url,
            'registration_number': bus_details.registration_number,
            'thumbnail': bus_details.thumbnail.url,
            'ac_nonac': bus_details.ac_nonac,
            'wifi': bus_details.wifi,
            'food': bus_details.food,
            'bus_route': {
                'start': bus_route.start,
                'destination': bus_route.destination,
                'starting_time': bus_route.starting_time,
                'destination_time': bus_route.destination_time,
            },
            'from_bus_point': {
                'stop_name': from_bus_point.stop_name,
                'stop_order': from_bus_point.stop_order,
                'arrival_time': from_bus_point.arrival_time,
                'price': from_bus_point.price,
            },
            'to_bus_point': {
                'stop_name': to_bus_point.stop_name,
                'stop_order': to_bus_point.stop_order,
                'arrival_time': to_bus_point.arrival_time,
                'price': to_bus_point.price,
            },
            'total_price': total_price,  # Include the total price in the JSON response
        }

        print("Bus details:", bus_details_json)

        return JsonResponse(bus_details_json)
    except BusDetails.DoesNotExist:
        # Return a 404 response if the bus ID does not exist
        return JsonResponse({'error': 'Bus not found'}, status=404)
    except BusRoute.DoesNotExist:
        # Return a 404 response if the route ID does not exist
        return JsonResponse({'error': 'Bus route not found'}, status=404)
    except BusPoints.DoesNotExist:
        # Return a 404 response if the bus point ID does not exist
        return JsonResponse({'error': 'Bus point not found'}, status=404)
    


@api_view(['POST'])
def save_seat_reservation(request):
    print("Seat reservation API HIT")
    if request.method == 'POST':
        bus_id = request.data.get('bus_id')
        print("Bus ID:", bus_id)
        
        route_id = request.data.get('route_id')
        print("Route ID:", route_id)
        
        from_bus_point_id = request.data.get('from_bus_point_id')
        print("From Bus Point ID:", from_bus_point_id)
        
        to_bus_point_id = request.data.get('to_bus_point_id')
        print("To Bus Point ID:", to_bus_point_id)
        
        user_id = request.data.get('user_id')
        print("User ID:", user_id)
        
        date = request.data.get('date')
        print("Date:", date)
        
        total = len(request.data.get('selected_seats', []))
        print("Total Seats:", total)
        
        payment_status = 'Pending'  # Set default payment status
        print("Payment Status:", payment_status)
        
        referral_code_used = request.data.get('referral_code_used')
        print("Referral Code Used:", referral_code_used)
        
        referred_user = request.data.get('referred_user')
        print("Referred User:", referred_user)
        
        pickup_id = request.data.get('pickup')
        print("Pickup ID:", pickup_id)
        
        dropoff_id = request.data.get('dropoff')
        print("Dropoff ID:", dropoff_id)
        
        selected_seats = request.data.get('selected_seats')
        print("Selected Seats:", selected_seats)

       

        try:
            pickup_point = BusPoints.objects.get(pk=pickup_id)  # Fetch the pickup point instance
            print("Pickup Point:", pickup_point)

            from_bus_point = BusPoints.objects.get(pk=dropoff_id)  # Fetch the from bus point instance
            print("From Bus Point:", from_bus_point)

            reservation = BusReservation.objects.create(
                bus_id=bus_id,
                user_id=user_id,
                date=date,
                total=total,
                payment_status=payment_status,
                referral_code_used=referral_code_used,
                referred_user=referred_user,
                pickup=pickup_point,  # Assign the pickup point instance
                dropoff=from_bus_point,  # Assign the from bus point instance
                # Add other fields as needed
            )
            print("Seat reservation saved successfully")
            print("Seat reservation saved successfully")
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error saving seat reservation:", e)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    

def check_seat_availability(request, from_bus_point_id, to_bus_point_id):
    try:
        print("check seat API HIT")
        # Retrieve reservations where pickup and dropoff points match the provided IDs
        reservations = BusReservation.objects.filter(pickup_id=from_bus_point_id, dropoff_id=to_bus_point_id)
        
        if reservations.exists():
            reserved_seats = set()
            for reservation in reservations:
                reservation_details = BusReservationDetails.objects.filter(reservation=reservation)
                reserved_seats.update([detail.seat_number for detail in reservation_details])
            print("Reserved seats:", reserved_seats)
            return JsonResponse({'reserved_seats': list(reserved_seats)})
        else:
            print("No reservations found for the provided bus points.")
            return JsonResponse({'reserved_seats': []})
    except Exception as e:
        print("An error occurred:", str(e))
        return JsonResponse({'message': 'An error occurred.'})


@csrf_exempt
def userlogin(request):
    if request.method == 'POST':

        receieved_data = json.loads(request.body)
        print(receieved_data)
        getemail = receieved_data["email"]
        getpassword = receieved_data["password"]
        data = list(UserProfile.objects.filter(Q(email__exact=getemail) & Q(password__exact=getpassword)).values())
        return HttpResponse(json.dumps(data)) 
    else:
        return HttpResponse(json.dumps({"status": "login details Invalid"}))  
    

def send_ticket_confirmation_to_email(email):
    subject = 'Ticket Confirmed'
    message = f'Your Ticket have been  Confirmed'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return True

    
@csrf_exempt
def save_bus_reservation(request):
    if request.method == 'POST':
        print("Save Bus Reservation API HIT")

        # Extract data from the request payload
        data = json.loads(request.body.decode('utf-8'))

        bus_id = data.get('bus_id')
        busname = data.get('busname')
        date = data.get('date')
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        route_id = data.get('route_id')
        selected_seats = data.get('selected_seats')
        passenger_details = data.get('passengerDetails')
        totalSEATS = data.get('totalSEATS')
        user_id = data.get('user_id')
        price = data.get('price')

        # Print received data for debugging
        print("Bus ID:", bus_id)
        print("Bus Name:", busname)
        print("Date:", date)
        print("From Bus pickup:", pickup)
        print("To Bus dropoff:", dropoff)
        print("To Bus route_id:", route_id)
        print("Selected Seats:", selected_seats)
        print("Passenger Details:", passenger_details)
        print("totalSEATS :", totalSEATS)
        print("user_id :", user_id)
        print("price :", price)

        total_price = price * totalSEATS

        reservation = BusReservation.objects.create(
                bus_id=bus_id,
                user_id=user_id,
                date=date,
                pickup_id=pickup,
                dropoff_id=dropoff,
                total=total_price,  # Calculated total price
                payment_status='Pending',  # Assuming payment status is initially set to 'Pending'
                referral_code_used=data.get('referral_code_used', '0'),
                referred_user=data.get('referred_user', '0')
            )
        
                    # Create BusReservationDetails instances for each passenger
        for index, seat in enumerate(selected_seats):
                passenger_detail = passenger_details[index]
                BusReservationDetails.objects.create(
                    reservation=reservation,
                    name=passenger_detail['name'],
                    age=passenger_detail['age'],
                    gender=passenger_detail['gender'],
                    ticket_number=f'PRN{index + 1}{user_id}',  # You can generate ticket number as per your requirement
                    seat_number=seat,
                    price=price  # Assuming each seat has the same price
                )

        user_email = UserProfile.objects.get(id=user_id)

        send_ticket_confirmation_to_email(user_email.email)

       
        return JsonResponse({"status": "Reservation details saved successfully"})
    else:
        return HttpResponse(json.dumps({"status": "Method not allowed"}), status=405)



@api_view(['GET'])
def user_reservation_details(request, email):
    try:
        print("User reservation details API HIT")
        # Get the user corresponding to the email
        user = UserProfile.objects.get(email=email)

        # Get reservations associated with the user
        reservations = BusReservation.objects.filter(user=user)
        print("reservations user :", reservations)
        
        serialized_reservations = []

        for reservation in reservations:
            # Fetch pickup and drop-off points for each reservation
            pickup_point = BusPoints.objects.get(id=reservation.pickup.id)
            dropoff_point = BusPoints.objects.get(id=reservation.dropoff.id)

            # Fetch route details for pickup and dropoff points
            pickup_route = pickup_point.route
            dropoff_route = dropoff_point.route

            # Fetch user profile associated with the reservation
            user_profile = reservation.user
            bus = reservation.bus

            # Construct route name using start and destination
            pickup_route_name = f"{pickup_route.start} to {pickup_route.destination}"
            print("pickup_route_name :", pickup_route_name)
            dropoff_route_name = f"{dropoff_route.start} to {dropoff_route.destination}"

            # Fetch bus staff details associated with the bus
            bus_staff = BusStaff.objects.filter(busowner=bus.busowner)

            # Serialize bus staff details
            serialized_bus_staff = []
            for staff in bus_staff:
                serialized_staff = {
                    "first_name": staff.first_name,
                    "last_name": staff.last_name,
                    "phone": staff.phone,
                    "type": staff.type
                }
                serialized_bus_staff.append(serialized_staff)

            serialized_reservation = {
                "id": reservation.id,
                "date": reservation.date,
                "total": reservation.total,
                "payment_status": reservation.payment_status,
                "referral_code_used": reservation.referral_code_used,
                "referred_user": reservation.referred_user,
                "pickup": {
                    "name": pickup_point.stop_name,
                    "route": pickup_route_name,
                    "time": pickup_point.arrival_time
                },
                "dropoff": {
                    "name": dropoff_point.stop_name,
                    "time": dropoff_point.arrival_time,
                    "route": dropoff_route_name
                },
                "user_profile": {
                    "first_name": user_profile.first_name,
                    "last_name": user_profile.last_name,
                    "phone": user_profile.phone,
                    "email": user_profile.email
                },
                "route":{
                    "route_name":pickup_route_name
                },
                "bus": {
                    "busname": bus.busname,
                    "staff": serialized_bus_staff  # Include bus staff details
                }
                
            }
            
            # Fetch passenger details for the reservation
            passenger_details = BusReservationDetails.objects.filter(reservation=reservation)
            serialized_passenger_details = []
            for detail in passenger_details:
                serialized_passenger_detail = {
                    "name": detail.name,
                    "age": detail.age,
                    "gender": detail.gender,
                    "ticket_number": detail.ticket_number,
                    "seat_number": detail.seat_number,
                    "price": detail.price
                }
                serialized_passenger_details.append(serialized_passenger_detail)

            # Add passenger details to the reservation
            serialized_reservation["passenger_details"] = serialized_passenger_details

            serialized_reservations.append(serialized_reservation)

        if not serialized_reservations:
            return JsonResponse({"message": "No reservations found for the user."}, status=404)

        return JsonResponse(serialized_reservations, safe=False)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except BusReservation.DoesNotExist:
        return JsonResponse({"error": "Reservations not found for the user"}, status=404)



#======= REFFERAL  =======================


@api_view(['GET'])
def check_referral_code(request, newReferralCode):
    print("Checking referral code API HIT Successfully")
    print("2nd Checking referral code API HIT Successfully")
    try:
        print("3rd Checking referral code API HIT Successfully")
        # Query UserProfile model to check if the referral code exists
        user_profiles = UserProfile.objects.filter(refferalcode=newReferralCode, refferalcode_status=0)
        print("Number of profiles found:", user_profiles.count())  
        
        print("newReferralCode :" , newReferralCode)
        
        if user_profiles.exists():
            print("User profiles found")  # Debugging: Print message indicating profiles were found
            for user_profile in user_profiles:
                email = user_profile.email
                print("email :", email)
                # If at least one UserProfile object is found, update their status to 1
                user_profile.refferalcode_status = 1
                user_profile.save()
                # Return the email
                return Response({'email': email}, status=200)
        else:
            print("No user profiles found")  # Debugging: Print message indicating no profiles were found
            # If no UserProfile objects are found, return status 404
            return Response({'detail': 'Referral code not found'}, status=404)
    except Exception as e:
        # Catch any other exceptions and print the error message for debugging
        print("Error:", e)
        return Response({'detail': 'An error occurred while processing the referral code'}, status=500)


@api_view(['GET'])
def check_user_email(request, email):
    try:
        print("API Endpoint Hit!")
        check_email = UserProfile.objects.filter(email=email).exists()
        response_data = {'exists': check_email}
        print("check_email:", response_data)
        return JsonResponse(response_data)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500) 
    
@api_view(['GET'])
def check_user_phone(request, phone):
    try:
        print("API Endpoint Hit!")
        check_phone = UserProfile.objects.filter(phone=phone).exists()
        response_data = {'exists': check_phone}
        print("check_phone:", response_data)
        return JsonResponse(response_data)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500) 


@api_view(['POST'])
def user_verify_otp(request):
    print("API HIT")
    
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body.decode('utf-8'))
            otp = int(received_data.get('otp'))
            firstName = received_data.get('firstName', '')  
            lastName = received_data.get('lastName', '')  
            email = received_data.get('email', '')  
            phone = received_data.get('phone', '')  
            password = received_data.get('password', '')  

            print("firstName:", firstName)
            print("lastName:", lastName)
            print("email:", email)
            print("phone:", phone)
            print("password:", password)

            # Check if the OTP exists in the database
            with transaction.atomic():
                otp_object = Otp.objects.select_for_update().filter(otp=otp, email=email).first()

                if otp_object:
                    # Check if the OTP is expired
                    if otp_object.is_expired:
                        response_data = {'status': 'expired'}
                    else:
                        # Check if the OTP is verified
                        if otp_object.is_verified:
                            response_data = {'status': 'already_verified'}
                        else:
                            # Check if the OTP is invalid
                            if not otp_object.is_valid():
                                # Increase the attempt count only for invalid attempts
                                otp_object.attempt += 1
                                otp_object.save()

                                # Check if the attempt limit has been reached (e.g., 5 attempts)
                                if otp_object.attempt >= 5:
                                    otp_object.is_expired = True  # Mark OTP as expired
                                    otp_object.save()
                                    response_data = {'status': 'attempt_limit_exceeded'}
                                else:
                                    response_data = {'status': 'invalid'}
                            else:
                                # Set the OTP status to 'verified'
                                otp_object.is_verified = True
                                otp_object.save()

                                random_number = random.randint(100, 999)
                                # Generate a random 3-digit number
                                refferalcode = f'RFR{random_number}'
                                bus_owner = UserProfile(first_name=firstName,last_name=lastName, email=email, phone=phone, password=password, refferalcode=refferalcode)
                                bus_owner.save()

                                response_data = {'status': 'verified', 'name': firstName, 'email': email, 'phone': phone, 'password': password}
                else:
                    response_data = {'status': 'invalid'}

            print("Response data:", response_data)
            return JsonResponse(response_data)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def send_otp_to_email(email, otp_code):
    subject = 'Your OTP for Signup'
    message = f'Your OTP for signup is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return True


@csrf_exempt
@api_view(["POST"])
def register(request):
    print("User Register Api hit")
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            print("Received data:", received_data)

            # Check if the email already exists
            if UserProfile.objects.filter(email=received_data['email']).exists():
                print("Email already exists")
                return JsonResponse({"status": "error", "message": "Email already exists"}, status=400)

            # Check if the phone number already exists
            if UserProfile.objects.filter(phone=received_data['phone']).exists():
                print("Phone number already exists")
                return JsonResponse({"status": "error", "message": "Phone number already exists"}, status=400)

            generated_otp = ''.join(random.choice('0123456789') for i in range(6))
            received_data['otp'] = generated_otp

            serializer = UserSignupSerializers(data=received_data)
            send_otp_to_email(received_data['email'], generated_otp)
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

def profile(request , sessionEmail):
    if request.method == 'GET':

        try:
            user_profile = UserProfile.objects.get(email=sessionEmail)
            # Convert user profile to JSON format
            profile_data = {
                'firstName': user_profile.first_name,
                'lastName': user_profile.last_name,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'password': user_profile.password  # Note: Storing password in plaintext is not recommended, consider hashing it
            }
            return JsonResponse(profile_data)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@api_view(['POST'])
def update_profile(request, sessionEmail):
    if request.method == 'POST':
        data = request.data
        email = sessionEmail  # Use the session email directly

        try:
            user_profile = UserProfile.objects.get(email=email)

            # Update the user profile fields based on the request data
            user_profile.first_name = data.get('firstName', user_profile.first_name)  # Use the existing value if not provided
            user_profile.last_name = data.get('lastName', user_profile.last_name)
            user_profile.phone = data.get('phone', user_profile.phone)

            # Save the updated user profile
            user_profile.save()

            return Response({'message': 'Profile updated successfully'})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
    



def fetch_user_referred_code(request, sessionName):
    print("Fetch user referred code API HIT")
    
    print("session_email ", sessionName)
    if sessionName:
        try:
            user_profile = UserProfile.objects.get(email=sessionName , refferalcode_status=0)
            referral_code = user_profile.refferalcode
            return JsonResponse({'referralCode': referral_code})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
    else:
        return JsonResponse({'error': 'Session email not found'}, status=400)