from django.contrib import admin
from .models import *


class BusDetailsAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'phone', 'email')
admin.site.register(BusOwner, BusDetailsAdmin)


