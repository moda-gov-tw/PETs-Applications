from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from general.models import ExecuteModel

from .models import VisitCountModel

import os
import shutil

import logging
from datetime import date
today = date.today()
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')

@login_required
def index(request):
    count_model = VisitCountModel.objects.filter(id=1)
    if count_model:
        count_model = count_model[0]
        count_model.count += 1
    else:
        count_model = VisitCountModel()
        count_model.count = 1
    count_model.save()
    
    request_dict = {}
    request_dict['count'] = count_model.count
    return render(request, 'home.html', request_dict)
    
class MaintainView(View):
    def get(self, request, *arg, **kwargs):
        for objects in ExecuteModel.objects.all():
            logging.info('maintain delect: ' + objects)
            objects.delete()
        return render(request, 'maintain/maintain_page.html')

class InitializeView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        username = request.user.get_username()
        if not username:
            raise Exception('username empty')
        finish = False
        for path in [settings.UPLOAD_ROOT, settings.OUTPUT_ROOT]:
            for method in os.listdir(path):
                temp_path = path+method+'/'+username+'/'
                if os.path.exists(temp_path):
                    for directory_path in os.listdir(temp_path):
                        shutil.rmtree(temp_path+directory_path)
        path = settings.DPVIEW_TEMP_ROOT+username+'/'
        if os.path.exists(path):
            for directory_path in os.listdir(path):
                shutil.rmtree(path+directory_path)
        if ExecuteModel.objects.filter(user_name=username).exists():
            file = ExecuteModel.objects.get(user_name=username)
            logging.info(username + 'initialize ExecuteModel')
            file.delete()
        finish = True
        return JsonResponse(finish, safe=False)