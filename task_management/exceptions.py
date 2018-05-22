from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

def handler500(request):
   
	status_code = 500
	message = "Server is currently unavailable"
	return JsonResponse({'message':message}, status=status_code)
	#return Response( status=status.HTTP_500_INTERNAL_SERVER_ERROR)