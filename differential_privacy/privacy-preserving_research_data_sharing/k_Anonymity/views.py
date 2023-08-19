from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from k_Anonymity import k_anonymity
from k_Anonymity.forms import ParameterForm

from general.views import AbstractMethodView
from general.views import AbstractExecuteView
from general.views import AbstractBreakProgramView

@login_required
def index(request):
    request_dict = {}
    request_dict['file_upload_url'] = reverse('k_Anonymity:file_upload', args=['json'])
    request_dict['custom_url'] = reverse('k_Anonymity:custom')
    request_dict['caller'] = 'k_Anonymity'
    return render(request, 'k_Anonymity/k_Anonymity_home.html', request_dict)
    
class KAnonymityView(AbstractMethodView):
    def get_form(self, requestContent):
        return ParameterForm(requestContent)
        
    def method_run(self, request):
        k_anonymity.run(request)
        
    def get_method_template(self):
        return 'k_Anonymity/k_Anonymity.html'
        
class BreakProgramView(AbstractBreakProgramView):
    def break_program(self, file):
        k_anonymity.break_program(file)
        
class ExecuteView(AbstractExecuteView):
    def get_empty_form(self):
        return ParameterForm()