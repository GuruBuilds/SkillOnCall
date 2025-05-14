from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def send_booking_email(subject, recipient_email, template, context):
    try:
        html_message = render_to_string(template, context)
        send_mail(subject, '', settings.EMAIL_HOST_USER, [recipient_email], html_message=html_message)
        return True, None
    except Exception as e:
        logger.exception(f"Email sending failed: {e}")
        return False, str(e)
