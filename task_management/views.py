import json
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import QueryDict
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from task_management.models import Milestone as milestone
from task_management.models import Task as task
from task_management.models import User as user
from task_management.models import User_login as user_login
from task_management.serializers import UserSerializer ,UserLoginSerializer, MilestoneSerializer , TaskSerializer
from .decorators import login_required
from .tokens import token_gen
from django.http import JsonResponse
import logging
from django.db.models import Min

logger = logging.getLogger(__name__)

class User(APIView):
	def post(self, request, format='json'):  
		serializer = UserSerializer(data=request.data)
		if not serializer.is_valid():
			logger.exception("serializer not valid")
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		user = serializer.save()
		logger.info("user saved")
		if not user:
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		current_site = get_current_site(request)
		message = render_to_string('acc_active_email.html', {
			'user':user, 
			'domain':current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token': token_gen.make_token(user),
		})
		mail_subject = 'Activate your account.'
		to_email = request.POST['email']
		email = EmailMessage(mail_subject, message, to=[to_email])
		email.send()
		logger.info("email sent")
		
        
class UserLogin(APIView):
	
	def post(self,request):
		try:
			db_user = user.objects.get(email=request.POST['email'])
		except:
			logger.exception("couldn't find user object")
			return Response("user doesn't exists", status=status.HTTP_400_BAD_REQUEST)
		if not db_user.check_password(request.POST['password']) or not  db_user.e_verification == True:
			logger.error("password didn't match or email verification wasn't done")
			return Response("password didn't match", status=status.HTTP_400_BAD_REQUEST)
		token = token_gen.make_token(db_user)
		serializer = UserLoginSerializer(data= {'user': db_user.id, 'last_login': timezone.now(),'token':token })
		if not serializer.is_valid():
			logger.error("data not valid")
			return Response("data is not valid", status=status.HTTP_400_BAD_REQUEST)
		db_user = serializer.save()
		logger.info("user saved")
		if db_user:
			return Response(serializer.data['token'], status=status.HTTP_200_OK)
	
class Milestone(APIView):
	
	def post(self, request, format='json'): 
		
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			logger.error("User is not valid")
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		data =request.POST.copy()
		data.update({'user': user[0].user_id}) 
		serializer = MilestoneSerializer(data=data)
		if not serializer.is_valid():
			logger.error("Serializer not valid")
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		ms = serializer.save()
		logger.info("Milestone saved")
		if ms:
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		
	def get(self, request, format=None):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		ms = milestone.objects.filter(user = user[0].user_id) 
		logger.info("Milestone related to user found")
		serializer = MilestoneSerializer(ms, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	
class MilestoneDetail(APIView):
	
	def get(self, request,milestone_id, format=None):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		ms = milestone.objects.filter(id =milestone_id, user = user[0].user_id) 
		logger.info("Milestone related to user found")
		serializer = MilestoneSerializer(ms, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def delete(self, request, milestone_id):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		ms = milestone.objects.get(id=milestone_id, user = user[0].user_id) 
		logger.info("Milestone related to user found")
		ms.delete()
		logger.info("Milestone deleted")
		return Response(status=status.HTTP_204_NO_CONTENT)
	
class Task(APIView):
	
	def post(self, request, milestone_id, format='json'):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		data =request.POST.copy()
		data.update({'milestone': milestone_id})
		serializer = TaskSerializer(data=data)
		if not serializer.is_valid():
			logger.error("Serializer Not valid")
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		task = serializer.save()
		logger.info("task saved")
		
		if task:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

	def get(self, request,milestone_id, format=None):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		tasks = task.objects.filter(milestone = milestone_id)
		logger.info("Task related to milestone found")
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
			
	
class TaskDetail(APIView):

	def get(self, request,milestone_id, task_id, format=None):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		tasks = task.objects.filter(milestone_id = milestone_id, id = task_id)
		logger.info("Particular Task related to milestone found")
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


	def delete(self, request,milestone_id, task_id ):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		tasks = task.objects.filter(milestone_id = milestone_id, id=task_id)
		logger.info("Particular Task related to milestone found")
		tasks.delete()
		logger.info("Task deleted")
		return Response(status=status.HTTP_204_NO_CONTENT)
	


class Reports(APIView):
	def get(self,request):
		user = user_login.objects.filter(token = request.META['HTTP_TOKEN'])
		if not user:
			return Response("Login to access this feature", status=status.HTTP_400_BAD_REQUEST)
		milestones = milestone.objects.filter(user = user[0].user_id)
		total_milestones = milestones.count()
		
		try:
			offset = int(request.GET.get('offset'))
		except:
			logger.info('Offset parameter not present')
			offset = 0
		try:
			total_count  = int(request.GET.get('count'))
		except:	
			logger.info('Count parameter not present')
			total_count  = total_milestones

		data = {}
		milestone_list = []
		logger.info('Getting total count of milestones of a user')
		data.update({'Total Count':total_milestones})
		for user_milestone in milestones[offset:total_count]:
			task_list = []
			Mserializer = MilestoneSerializer(user_milestone)
			tasks = task.objects.filter(milestone = user_milestone.id)
			for user_task in tasks:
				Tserializer = TaskSerializer(user_task)
				task_list.append(Tserializer.data)
			ms = Mserializer.data
			logger.info('Appending Task in milestones')
			ms.update({'Task':task_list})
			milestone_list.append(ms)
		logger.info('Appending Milestones in list')
		data.update({'Milestone':milestone_list})
		return Response(data, status= status.HTTP_400_BAD_REQUEST )	

class ReportPending(APIView):
	def get(self,request,format=None):
		max_pending = 0
		max_pending_user = 0
		users = user.objects.all()
		for db_user in users:
			pending = 0
			milestones = milestone.objects.filter(user = db_user.id)
			for user_milestone in milestones:
				tasks = task.objects.filter(milestone = user_milestone.id)
				for user_task in tasks:
					if user_task.status != 'complete':
						pending +=1
			if pending > max_pending:
				max_pending = pending
				max_pending_user = db_user
		serializer = UserSerializer(max_pending_user)
		data = serializer.data
		data.update({'Total_pending': max_pending})
		return Response(data, status=status.HTTP_200_OK)
		
class ReportCompleted(APIView):
	def get(self,request):
		start_date = int(request.GET.get('start_date'))
		end_date  = int(request.GET.get('end_date'))
		tasks = task.objects.filter(status = 'complete', end_date__lte=end_date, end_date__gte=start_date)
		logger.info('Tasks satisfying the condition, returned from database')
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
		
class ReportOldest(APIView):
	def get(self,request,format=None):
		tasks = task.objects.order_by('start_date')[0]
		logger.info('Oldest task, returned from database')
		serializer = TaskSerializer(tasks)
		return Response(serializer.data, status=status.HTTP_200_OK)
		

