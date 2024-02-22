from django.contrib import admin
from . models import *

class RefferalAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user','code', 'referred_bus' , 'expiration_date')
admin.site.register(ReferralCode, RefferalAdmin)