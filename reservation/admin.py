from django.contrib import admin
from . models import *

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user','buspoint' , 'date', 'total', 'payment_status', 'referral_code_used', 'referred_user')
admin.site.register(BusReservation, ReservationAdmin)

class ReservationDetailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'reservation','name' , 'age', 'gender', 'ticket_number', 'seat_number', 'price')
admin.site.register(BusReservationDetails, ReservationDetailsAdmin)