from django.urls import path
from . import views

urlpatterns = [
    path('check_file_status/', views.CheckFileStatus.as_view(), name = 'check_file_status'),
]