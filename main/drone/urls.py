# ./employee/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check/<str:license>/', views.Users_List, name='User_list'),
    path('issueTicket', views.issueTicket, name = 'Issue_Ticket' )
]