from django.urls import path
from . import views
from .admin import VoterAdmin

app_name = 'voters'

urlpatterns = [
    path('list/', views.voter_list, name='voter-list'),
    path('api/filter-voters/', views.filter_voters, name='filter-voters'),
    path('admin/voters/voter/api/bulk-delete/', VoterAdmin.bulk_delete_voters, name='admin:bulk-delete-voters'),
    path('admin/voters/send-notification/', views.send_notification, name='send-notification'),
]