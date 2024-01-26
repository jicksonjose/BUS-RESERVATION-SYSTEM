from django.contrib import admin
from .models import *


class BusDocumentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'busowner', 'busRc', 'owner_ID')
admin.site.register(BusDocument, BusDocumentsAdmin)

class BusDetailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'busowner', 'busname', 'thumbnail', 'busnumber', 'seats')
admin.site.register(BusDetails, BusDetailsAdmin)

class BusFeatureAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bus', 'title', 'description')
admin.site.register(BusFeature, BusFeatureAdmin)

class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bus', 'source','destination', 'price')
admin.site.register(BusRoutes, BusRouteAdmin)


class BusPointAdmin(admin.ModelAdmin):
    list_display = ('pk', 'route','starting_point',  'destination_point', 'price' )
    ordering = ['created_at',]
admin.site.register(BusPoints, BusPointAdmin)

class BusNumberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'busowner','busnumber' )

admin.site.register(BusNumber, BusNumberAdmin)


