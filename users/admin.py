from django.contrib import admin
from .models import *


class BusDetailsAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'phone', 'email')
admin.site.register(BusOwner, BusDetailsAdmin)

class OtpAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'email', 'otp', 'attempt')
admin.site.register(Otp, OtpAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','first_name', 'last_name', 'phone', 'email', 'password','refferalcode','refferalcode_status')
admin.site.register(UserProfile, UserProfileAdmin)


