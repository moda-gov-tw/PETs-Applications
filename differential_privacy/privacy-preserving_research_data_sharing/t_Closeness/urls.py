from django.urls import path
from . import views
from general import views as general_views
from json_parser import views as json_parser_views
from . import t_closeness

app_name = 't_Closeness'
urlpatterns = [
    path('', views.index, name = 'home'),
    path('execute', views.TClosenessView.as_view(), name = 'execute'),
    path('break_program/', views.BreakProgramView.as_view(), name = 'break_program'),
    path('show_progress/', t_closeness.show_progress, name = 'show_progress'),
    path('execute_page/<str:csv_name>/', views.ExecuteView.as_view(), name = 'execute_page'),
    path('custom/', json_parser_views.CustomView.as_view(), name = 'custom'),
    path('custom/<str:csv_name>/', json_parser_views.CustomView.as_view()),
    path('create_json/', json_parser_views.ParserView.as_view(), name = 'create_json'),
    path('advanced_settings/<str:csv_name>/', json_parser_views.AdvancedSettingsView.as_view(), name = 'advanced_settings'),
]

general_patterns = [
    path('file_upload/<str:mode>', general_views.FileView.as_view(), name = 'file_upload'),
    path('download_output/<str:csv_name>/', general_views.DownloadView.as_view(), name = 'download_output'),
    path('display_<str:method>/', general_views.DisplayCsvView.as_view(), name = 'display'),
    path('check_utility/', general_views.CheckUtilityView.as_view(), name = 'check_utility'),
    path('check_utility/<str:select_mode>', general_views.CheckUtilityView.as_view()),
    path('title_check/', general_views.TitleCheckView.as_view(), name = 'title_check'),
    path('finish/<str:csv_name>/', general_views.FinishView.as_view(), name = 'finish'),
    path('utility_page/<str:csv_name>/', general_views.UtilityPageView.as_view(), name = 'utility_page'),  
]

urlpatterns.extend(general_patterns)