from django.urls import path
from . import views

urlpatterns = [
  
    path('add_bus_details/', views.add_bus_details , name='add_bus_details'),
    path('bus-details-list/', views.bus_details_list , name='bus-details-list'),
    path('get_bus_details_and_routes/<int:owner_id>/', views.get_bus_details_and_routes, name='get_bus_details_and_routes'),
    path('save_schedule/', views.save_schedule, name='save_schedule'),
    
    
   
  
]
