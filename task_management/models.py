from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    
    use_in_migrations = True
    """Create and save a User with the given email and password."""
    
    def create_user(self, email=None, password=None, e_verification = False):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, e_verification = e_verification) 
        user.set_password(password)
        user.save(using=self._db)
        return user   

class User(AbstractUser):
    is_active   = None
    is_staff    = None
    is_superuser= None
    last_name   = None
    first_name  = None
    last_login  = None
    date_joined = None
    username    = None
    e_verification = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'User'


class Milestone(models.Model):
    STATUS_CHOICES = (
    ('COMPLETE', 'complete'),
    ('INPROGRESS', 'Inprogress'),
    ('IDLE', 'Idle'),)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=30)
    target_date = models.DateField(auto_now_add=False)
    status      = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Idle')
    class Meta:
        db_table = 'Milestone' 

class Task(models.Model):
    STATUS_CHOICES = (
    ('COMPLETE', 'complete'),
    ('INPROGRESS', 'Inprogress'),
    ('IDLE', 'Idle'),)
    
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    title     = models.CharField(max_length=30)
    status    = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Idle',)
    start_date= models.DateField(auto_now_add=False)
    end_date  = models.DateField(auto_now_add=False)
    class Meta:
        db_table = 'Task' 

class User_login(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_login  = models.DateTimeField(default = timezone.now)
    token       = models.CharField(default=None, max_length=30)
    class Meta:
        db_table = 'User_login'
