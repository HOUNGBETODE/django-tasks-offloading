from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.conf import settings
from celery import shared_task
import pyotp
import jwt

logger = get_task_logger(__name__)

@shared_task
def sharedtask():
    return

@shared_task
def add_numbers(x, y):
    return x + y

@shared_task
# function to send mail to user from our app
def send_mail_to(userName, emailAddress, otpCode):
    logger.INFO(f"send_mail_to is on the way")
# defining :
    # - email subject
    subject = 'TePlay | User email verification'
    # - email sender
    from_email = settings.EMAIL_HOST_USER
    # - email receiver
    to_email = [emailAddress] 
# loading the HTML template and passing it user mail and otp code
    html_template = get_template('email.html')
    html_content = html_template.render({'name': userName, 'otp_code': otpCode})
# creating the email message, setting the content-type, and sending it
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
