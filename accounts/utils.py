#Varification Mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

from accounts.models import User


def send_activation_mail(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    to_email = user.email
    subject = "Activate your account"
    message =render_to_string("accounts/emails/verification_email.html",{
        'user' : request.user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    })
    send_email = EmailMessage(subject, message, from_email, to=[to_email])
    send_email.send()
    print("email sent")


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if (isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message,from_email,  to=to_email)
    mail.content_subtype = "html"
    mail.send()


def send_contact_email(mail_subject, mail_template, context):
    admin_info = User.objects.get(is_admin= True)
    admin_email = admin_info.email
    message = render_to_string(mail_template, context)
    
    mail = EmailMessage(mail_subject, message, to=[admin_email])
    mail.content_subtype = "html"
    mail.send()

def send_varification_email(request, user, mail_subject, email_template):
# ACCOUNT ACTIVATION
    
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,{
        'user' : user,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'domain' : current_site,
        'token' : default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message,from_email,  to=[to_email])
    mail.content_subtype = "html"
    mail.send()
