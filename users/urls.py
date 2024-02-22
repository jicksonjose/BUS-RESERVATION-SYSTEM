from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('get_email/<str:email>/', views.get_email, name="get_email"),
    path('check_phone/<str:phone>/', views.check_phone, name="check_phone"),
    path('verify-otp/', views.verify_otp, name="verify-otp"),
  
]
