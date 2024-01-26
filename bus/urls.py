from django.urls import path
from . import views

urlpatterns = [
    path('add_bus_document/', views.add_bus_document, name="add_bus_document"),
    path('add_bus_details/', views.add_bus_details , name='add_bus_details'),
    path('get_bus_numbers/<int:busowner>/', views.get_bus_numbers, name='get_bus_numbers'),
   
  
]
