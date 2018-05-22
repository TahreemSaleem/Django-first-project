from task_management.models import User_login as user_login
from rest_framework.response import Response
from rest_framework import status
def login_required(f):
    def wrap(self,request,user=0, *args, **kwargs):
        user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
        if not user:
            return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
        return f(self,request, user, *args, **kwargs)
    return wrap