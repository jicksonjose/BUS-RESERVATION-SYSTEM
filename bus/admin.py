from django.contrib import admin
from .models import *


class BusDocumentsAdmin(admin.ModelAdmin):
    list_display = ('pk','busname', 'busowner', 'busrc', 'registration_number','thumbnail','ac_nonac', 'wifi','food','drink', 'is_verified')
admin.site.register(BusDetails, BusDocumentsAdmin)


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bus', 'start','destination', 'starting_time','destination_time')
admin.site.register(BusRoute, BusRouteAdmin)

class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bus', 'route','date')
admin.site.register(BusSchedule, BusScheduleAdmin)

class BusPointsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'route', 'stop_name','stop_order','arrival_time', 'price' )
admin.site.register(BusPoints, BusPointsAdmin)

class BusStaffAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name','phone','type')
admin.site.register(BusStaff, BusStaffAdmin)

class BusStaffScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'staff', 'bus_schedule')
admin.site.register(BusStaffSchedule, BusStaffScheduleAdmin)

