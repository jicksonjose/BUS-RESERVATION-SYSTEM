from django.urls import path
from . import views

urlpatterns = [
  
    path('add_bus_details/', views.add_bus_details , name='add_bus_details'),
    path('bus-details-list/<int:owner_id>/', views.bus_details_list , name='bus-details-list'),
    path('get_bus_details_and_routes/<int:owner_id>/', views.get_bus_details_and_routes, name='get_bus_details_and_routes'),
    path('save_schedule/', views.save_schedule, name='save_schedule'),
    path('get_bus_details/<int:owner_id>/', views.get_bus_details, name='get_bus_details'),
    path('save_bus_route/', views.save_bus_route, name='save_bus_route'),
    path('bus-route-list/<int:owner_id>/', views.bus_route_list, name='bus-route-list'),
    path('bus-schedule-list/<int:owner_id>/', views.bus_schedule_list, name='bus-schedule-list'),
    path('add_bus_point/', views.add_bus_point, name='add_bus_point'),
    path('existing-stop-orders/<uuid:route_id>/<int:stop_order>/', views.existing_stop_orders, name='existing-stop-orders'),
    path('bus-points/<int:owner_id>/', views.bus_points, name='bus-points'),
    path('check_schedule_existence/<uuid:route>/', views.check_schedule_existence, name='check_schedule_existence'),
    path('add-bus-staff/', views.add_bus_staff, name='add-bus-staff'),
    path('bus-staff-list/<int:owner_id>/', views.bus_staff_list, name='bus-staff-list'),
    path('get-bus-staff/<int:owner_id>/', views.get_bus_staff, name='get-bus-staff'),
    path('get-bus-schedule/<int:owner_id>/', views.get_bus_schedule, name='get-bus-schedule'),
    path('add-bus-schedule/', views.add_bus_staff_schedule, name='add-bus-schedule'),
    path('check-staff-schedule-existence/<int:staff_id>/', views.check_staff_schedule_existence, name='check_staff_schedule_existence'),
    path('bus-staff-schedule-list/<int:owner_id>/', views.bus_staff_schedule_list, name='bus-staff-schedule-list'),
    path('bus-reservation/<int:owner_id>/', views.get_bus_reservations, name='bus-reservation'),
    path('bus-reservation-bus-details/<int:id>/', views.get_bus_reservations_bus_details, name='bus-reservation-bus-details'),
    path('bus_reservation_route_details/<uuid:route_id>/', views.bus_reservation_route_details, name='bus_reservation_route_details'),
    path('reservation-details/<int:id>/', views.reservation_details, name='reservation-details'),
    path('check-arrival-time-validity/<uuid:busRouteId>/<str:encodedTime>/', views.check_arrival_time_validity, name='check-arrival-time-validity'),

    
    
   
  
]
