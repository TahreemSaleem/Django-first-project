from django.contrib.auth.models import User 
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import token_gen
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from task_management.models import User

def activate(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)

    if user is not None and token_gen.check_token(user, token):
        user.e_verification = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')