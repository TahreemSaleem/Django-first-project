from django.conf.urls import url, handler500
from django.urls import path , include
import task_management.exceptions
from task_management.views import User, Milestone,MilestoneDetail, Task, TaskDetail, UserLogin
from django.contrib.auth import views as auth_views
from task_management.activate_account import activate

handler500 = task_management.exceptions.handler500

urlpatterns = [
    path('api/users/', task_management.views.User.as_view()), 
    path('api/users/login/',task_management.views.UserLogin.as_view()),


    path('api/milestones/', task_management.views.Milestone.as_view()),
    path('api/milestones/<int:milestone_id>/',  task_management.views.MilestoneDetail.as_view()),
    
    path('api/milestones/<int:milestone_id>/tasks/', task_management.views.Task.as_view()),
    path('api/milestones/<int:milestone_id>/tasks/<int:task_id>/',  task_management.views.TaskDetail.as_view()),
    
    path('api/reports/pending/', task_management.views.ReportPending.as_view()),
    path('api/reports/completed/<start_date>/<end_date>/', task_management.views.ReportCompleted.as_view()),
    path('api/reports/oldest/', task_management.views.ReportOldest.as_view()),
    
    path('api/reports/', task_management.views.Reports.as_view()),
    
    path('activate/<uidb64>/<token>/',task_management.activate_account.activate, name='activate'),

    ]
