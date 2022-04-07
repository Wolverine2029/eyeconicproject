# ./employee/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Users_List, name='User_list'),
    path('create/', views.create_user, name='Create_User'),
    path('delete/<int:id>', views.delete_user, name='Delete_User'),
    path('update/<int:id>', views.edit_user, name='Edit_User'),
    path('issueTicket', views.issueTicket, name = 'Issue_Ticket' )
]