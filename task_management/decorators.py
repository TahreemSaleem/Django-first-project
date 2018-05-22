from task_management.models import User_login as user_login
from rest_framework.response import Response
from rest_framework import status
def login_required(f):
    def wrap(request, *args, **kwargs):
        user = user_login.objects.filter(token = request.META['access_token'])
        if not user:
            return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
        return f(request, *args, **kwargs)
    return wrap