
from django.core.mail import send_mail
import uuid
from django.conf import settings

def send_otp_to_email(email, otp_code):
    subject = 'Your OTP for Signup'
    message = f'Your OTP for signup is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True

