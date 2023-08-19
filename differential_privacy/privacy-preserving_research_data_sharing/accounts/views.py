from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.views import View
from django.conf import settings
from django.utils.translation import gettext
from django.urls import reverse

from accounts.forms import TwUserCreationForm, ChangePasswordForm
import os
import shutil

class SignUpView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            self.accounts_init(username)
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/signup.html', {'form': form})
               
    def get(self, request, *arg, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = TwUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    
    def accounts_init(self, username):
        function_name = ['DPView', 'k_Anonymity', 'l_Diversity', 't_Closeness']
        for name in function_name:
            os.makedirs(settings.UPLOAD_ROOT+name+'/'+username+'/')
            os.makedirs(settings.OUTPUT_ROOT+name+'/'+username+'/')
        os.makedirs(settings.DPVIEW_TEMP_ROOT+username+'/')
        
class LogInView(View):
    def post(self, request, *arg, **kwargs):
        form = TwUserCreationForm(request.POST)
        username = request.POST.get('username', None)
        raw_password = request.POST.get('password1', None)
        referer = request.META.get('HTTP_REFERER')
        
        user = auth.authenticate(username=username, password=raw_password)
        if user is None:
            return render(request, 'registration/login.html',\
                {'form': form, 'error_message': gettext('帳密錯誤')})
        if not user.is_active:
            return render(request, 'registration/login.html',\
                {'form': form, 'error_message': gettext('帳戶已被凍結')})
        auth.login(request, user)
        
        next_page = 'home'
        if referer.find('next') != -1:
            next_page = referer.split('next=')[-1]
        return redirect(next_page)
        
    def get(self, request, *arg, **kwargs):
        next_page = request.GET.get('next', 'home')
        if request.user.is_authenticated:
            return redirect(next_page)
        form = TwUserCreationForm()
        return render(request, 'registration/login.html', {'form': form})
    
class LogOutView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        auth.logout(request)
        return redirect('login')
        
class DeleteAccountView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        user = request.user
        username = user.get_username()
        if not username:
            raise Exception('username empty')
        for path in [settings.UPLOAD_ROOT, settings.OUTPUT_ROOT]:
            for method in os.listdir(path):
                temp_path = path+method+'/'+username+'/'
                if os.path.exists(temp_path):
                    shutil.rmtree(temp_path)
        path = settings.DPVIEW_TEMP_ROOT+username+'/'
        if os.path.exists(path):
            shutil.rmtree(path)
        user.delete()
        return redirect('home')
        
class PasswordCheckView(View):
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        user = request.user
        password = request.POST.get('password', None)
        username = user.get_username()
        check = auth.authenticate(username=username, password=password)
        if check is None:
            return JsonResponse({'message':gettext('密碼錯誤，動作已取消')}, status=401)
        if not check.is_active:
            return JsonResponse({'message':gettext('帳戶已被凍結，動作已取消')}, status=401)
        return HttpResponse(status=204)
        
class PasswordCheckPageView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        mode = kwargs.get('mode')
        
        if mode == 'delete_account':
            cell_content = gettext('帳號即將刪除，刪除後資料無法回復，如確定要刪除請輸入密碼')
            check_success_action_url = reverse('delete_account')
        elif mode == 'change_password':
            cell_content = gettext('請輸入原本的密碼，以繼續進行密碼更改')
            check_success_action_url = reverse('change_password')
        else:
            raise Exception('PasswordCheckPageView mode error mode : '+mode)
        
        request_dict = {}
        request_dict['cell_content'] = cell_content
        request_dict['check_success_action_url'] = check_success_action_url
        return render(request, 'general/input_password_page.html', request_dict)        

class ChangePasswordView(View):
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        user = request.user
        username = user.get_username()
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            account = User.objects.get(username__exact=username)
            account.set_password(form.cleaned_data.get('password1'))
            account.save()
            auth.login(request, account)
            return redirect('home')
        else:
            return render(request, 'registration/change_password.html', {'form': form})
            
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        form = ChangePasswordForm()
        return render(request, 'registration/change_password.html', {'form': form})