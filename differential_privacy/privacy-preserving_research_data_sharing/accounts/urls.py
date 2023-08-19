from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('login/', views.LogInView.as_view(), name = 'login'),
    path('logout/', views.LogOutView.as_view(), name = 'logout'),
    path('delete_account/', views.DeleteAccountView.as_view(), name = 'delete_account'),
    path('change_password/', views.ChangePasswordView.as_view(), name = 'change_password'),
    path('password_check/', views.PasswordCheckView.as_view(), name = 'password_check'),
    path('password_check_page/<str:mode>/', views.PasswordCheckPageView.as_view(), name = 'password_check_page'),
]