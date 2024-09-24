from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

class AppHelper:

    def datetime():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def send_notification_email(user_email, subject, message):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
