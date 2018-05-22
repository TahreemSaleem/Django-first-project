from django.conf.urls import url, handler500
from django.urls import path , include
import task_management.exceptions
from task_management.views import User, Milestone,MilestoneDetail, Task, TaskDetail, UserLogin
from django.contrib.auth import views as auth_views
from task_management.activate_account import activate
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Task Management System API's")

handler500 = task_management.exceptions.handler500

urlpatterns = [
    path('',schema_view),

#   """User Registeration [POST]
    path('api/users/', task_management.views.User.as_view()), 

#   """" User Login [GET]"""
    path('api/users/login/',task_management.views.UserLogin.as_view()),

#    """Milestone creation and retrieval [POST,GET]"""
    path('api/milestones/', task_management.views.Milestone.as_view()),

#    """Milestone deletion and retrieval [DELETE,GET]"""
    path('api/milestones/<int:milestone_id>/',  task_management.views.MilestoneDetail.as_view()),

#    """Task creation and retrieval [POST,GET]"""
    path('api/milestones/<int:milestone_id>/tasks/', task_management.views.Task.as_view()),

#    """Task deletion and retrieval [DELETE,GET]"""
    path('api/milestones/<int:milestone_id>/tasks/<int:task_id>/',  task_management.views.TaskDetail.as_view()),

#    """Pending Reports retrieval [GET]"""
    path('api/reports/pending/', task_management.views.ReportPending.as_view()),

#    """Completed Reports retrieval with start_date and end_date parameters[GET]"""
    path('api/reports/completed/', task_management.views.ReportCompleted.as_view()),

#    """Oldest Reports retrieval [GET]"""
    path('api/reports/oldest/', task_management.views.ReportOldest.as_view()),

#    """Reports retrieval with offset and count parameters [GET]"""
    path('api/reports/', task_management.views.Reports.as_view()),

#    """Search Tasks through search term as parameter [GET]"""
    path('api/search/', task_management.views.Search.as_view()),

#    """Activation link in user's email [GET]"""
    path('activate/<uidb64>/<token>/',task_management.activate_account.activate, name='activate'),

    ]
