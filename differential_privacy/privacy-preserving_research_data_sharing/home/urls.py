from django.urls import path
from . import views
from general import views as general_views

urlpatterns = [
    path('', views.index, name='home'),
    path('initialize/', views.InitializeView.as_view(), name='initialize'),
    path('update_log/', general_views.UpdateLogView.as_view(), name = 'update_log'),
    path('file_finish/', general_views.FileFinishView.as_view(), name = 'file_finish'),
    path('file_running/', general_views.FileRunningView.as_view(), name = 'file_running'),
]