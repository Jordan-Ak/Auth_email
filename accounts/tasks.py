import secrets
from django.utils import timezone
from celery import shared_task
from celery.decorators import task  


from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

logger = get_task_logger(__name__)

@shared_task
def email_verification_flow(email, token) -> None:  # To send verification email
    #user = get_user_model().objects.get(id=user.id)
    #user.generate_email_verification_token()
    mail_message = 'This is your email verification link'
    send_mail(
        'Email Verification at AUTH',
         f'{mail_message}  http://127.0.0.1:8000/accounts/verify_mail/{token}',
        'from admin@email.com',
        [f'{email}'],
        fail_silently = False,)

@shared_task
def password_send_mail(email, token) -> None:
    mail_message = 'This is your Password Reset link'
    send_mail(
        'Password Reset at AUTH',
        f'{mail_message}  http://127.0.0.1:8000/accounts/password/reset/{token}/',
        'from admin@email.com',
        [f'{email}'],
        fail_silently = False,)

@shared_task
def generate_verification_token_sh() -> str:
    verification_token = secrets.token_urlsafe(50)
    #email_token_sent_at = timezone.now()
    return verification_token
      
@shared_task
def add(a,b):
    print(a+b)
    

