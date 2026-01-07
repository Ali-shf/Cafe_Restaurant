from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
import random
from authentication.models import CustomUser


def send_otp_via_email(email):
    try:
        otp = random.randint(100000, 999999)
        subject = 'Your account verification code'
        message = f'Your OTP for email verification: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
        )
        user_obj, created = CustomUser.objects.get_or_create(email=email)
        # user_obj.otp = otp
        user_obj.save()
        return True, "OTP sent successfully"
    except ObjectDoesNotExist:
        return False, "User not found"
    except Exception as e:
        return False, str(e)
    

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()