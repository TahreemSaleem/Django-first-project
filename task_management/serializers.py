from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from task_management.models import Milestone ,Task, User, User_login
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer): 
    email     = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password  = serializers.CharField(min_length=8, write_only=True)
    e_verification = serializers.BooleanField(default= False, write_only = True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],validated_data['password'],validated_data['e_verification'])
        return user

    class Meta:
        model   = User
        fields  = ('id', 'email', 'password', 'e_verification')

class UserLoginSerializer(serializers.ModelSerializer): 
    last_login = serializers.DateTimeField()
    token = serializers.CharField()
    class Meta:
        model  = User_login
        fields = ('id','last_login','user','token')

class MilestoneSerializer(serializers.ModelSerializer): 
    title       = serializers.CharField(required=True)
    target_date = serializers.DateField()
    status      = serializers.CharField(max_length=32)
    class Meta:
        model  = Milestone
        fields = ('id', 'title','target_date', 'status','user')

class TaskSerializer(serializers.ModelSerializer): 
    title       = serializers.CharField(required=True)
    status      = serializers.CharField(max_length=32)
    
    class Meta:
        model  = Task
        fields = ('id', 'title','status','milestone','end_date','start_date')