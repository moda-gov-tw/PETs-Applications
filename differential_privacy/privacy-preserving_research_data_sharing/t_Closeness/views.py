from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from t_Closeness import t_closeness
from t_Closeness.forms import ParameterForm

from general.views import AbstractMethodView
from general.views import AbstractExecuteView
from general.views import AbstractBreakProgramView

@login_required
def index(request):
    request_dict = {}
    request_dict['file_upload_url'] = reverse('t_Closeness:file_upload', args=['t_Closeness'])
    request_dict['custom_url'] = reverse('t_Closeness:custom')
    request_dict['caller'] = 't_Closeness'
    return render(request, 't_Closeness/t_Closeness_home.html', request_dict)

class TClosenessView(AbstractMethodView):
    def get_form(self, requestContent):
        return ParameterForm(requestContent)
        
    def method_run(self, request):
        t_closeness.run(request)
        
    def get_method_template(self):
        return 't_Closeness/t_Closeness.html'
    
class BreakProgramView(AbstractBreakProgramView):
    def break_program(self, file):
        t_closeness.break_program(file)
    
class ExecuteView(AbstractExecuteView):
    def get_empty_form(self):
        return ParameterForm()