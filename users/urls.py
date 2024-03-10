from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('get_email/<str:email>/', views.get_email, name="get_email"),
    path('check_phone/<str:phone>/', views.check_phone, name="check_phone"),
    path('verify-otp/', views.verify_otp, name="verify-otp"),
    path('check-user-email/<str:email>/', views.check_user_email, name="check-user-email"),
    path('check-user-phone/<int:phone>/', views.check_user_phone, name="check-user-phone"),
    path('user-verify-otp/', views.user_verify_otp, name="user-verify-otp"),
    path('register/', views.register, name="register"),
    path('profile/<str:sessionEmail>/', views.profile, name="profile"),
    path('update-profile/<str:sessionEmail>/', views.update_profile, name="update-profile"),

    path('userlogin/', views.userlogin, name="userlogin"),
    path('save-bus-reservation/', views.save_bus_reservation, name="save-bus-reservation"),

    

    path('bus_search_list/', views.bus_search_list, name="bus_search_list"),
    path('stopnames/', views.bus_stop_name, name="stopnames"),
    path('search_buses/', views.search_buses, name='search_buses'),
    path('bus-book-seat/<int:bus_id>/<uuid:route_id>/<uuid:from_bus_point_id>/<uuid:to_bus_point_id>/', views.bus_book_seat, name='bus-book-seat'),
    path('save-seat-reservation/', views.save_seat_reservation, name='save_seat_reservation'),
    path('check-seat-reservation/<uuid:from_bus_point_id>/<uuid:to_bus_point_id>/', views.check_seat_availability, name='check-seat-reservation'),
    path('get-reservation-details/<str:email>/', views.user_reservation_details, name='get-reservation-details'),
    path('check-referral-code/<str:newReferralCode>/', views.check_referral_code, name='check-referral-code'),
    path('fetch_user_referred_code/<str:sessionName>/', views.fetch_user_referred_code, name='fetch_user_referred_code'),


  
]
