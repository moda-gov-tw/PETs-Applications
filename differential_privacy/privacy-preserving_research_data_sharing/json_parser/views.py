from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.urls import reverse
from django.views import View

from general.function import DataframeDetection
from general.function import Path
from general.exception import PairLoopException
from general.exception import NotAddressException

from json_parser.json_parser import JsonParser
import json

import logging
from datetime import date
today = date.today()
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')

class ParserView(View):
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        username = request.user.get_username()
        file_name = request.POST.get('csv_name', None)
        structure_mode = json.loads(request.POST.get('structure_mode', None))
        structure_dict = json.loads(request.POST.get('structure_dict', None))
        interval_dict = request.POST.get('interval_dict', None)
        type_pair = request.POST.get('type_pair', None)
        
        if type_pair:
            type_pair = json.loads(type_pair)
        caller = path.get_caller(request)
        file_path = path.get_upload_root(request, caller=caller)
        
        try:
            for key in structure_mode:
                if structure_mode[key] == 'custom':
                    structure_dict[key] = self.pair_check(structure_dict[key])
            if interval_dict:
                interval_dict = json.loads(interval_dict)
            parser.create_json_file(file_path, file_name,
                structure_mode, structure_dict,
                type_pair=type_pair,
                interval_dict=interval_dict,)
        except NotAddressException as e:
            return JsonResponse({"message":str(e)}, status=400)
        except PairLoopException as e:
            return JsonResponse({"message":str(e)}, status=400)
        except Exception as e:
            logging.critical(username + ' ParserView run fail', exc_info=True)
            return JsonResponse({"message":gettext("程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務")}, status=404)
        else:
            logging.info(username + ' ParserView run success')
            return HttpResponse(status=204)
        logging.critical(username + ' unknown error', exc_info=True)
        return JsonResponse({"message":gettext("有尚未捕捉到的例外，請回報服務人員，謝謝")}, status=404)
    
    def pair_check(self, pair_dict):
        for key in list(pair_dict.keys()):
            value = pair_dict[key]
            previous_value = value
            ancestor_set = set()
            ancestor_set.add(value)
            while value in pair_dict:
                value = pair_dict[value]
                if previous_value == value:
                    return pair_dict
                if value in ancestor_set:
                    temp = ""
                    for element in ancestor_set:
                        temp = temp + element + ', '
                    raise PairLoopException(gettext("配對關係出現循環，將導致程式無限執行，請重新配對下列欄位：") + temp)
                previous_value = value
                ancestor_set.add(value)
            pair_dict[value] = value
        return pair_dict

class DPViewParserView(View):
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        username = request.user.get_username()
        file_path = str(request.POST.get('path', None))
        file_name = str(request.POST.get('csv_name',None))
        pair_dict = request.POST.get('number_title_pair_dict', None)
        almost_number_dict = request.POST.get('almost_number_dict', None)
        almost_number_is_empty_dict = request.POST.get('almost_number_is_empty_dict', None)
        interval_dict = request.POST.get('interval_dict', None)
        type_pair = request.POST.get('type_pair', None)
        
        if pair_dict:
            pair_dict = json.loads(pair_dict)            
        if almost_number_dict:
            almost_number_dict = json.loads(almost_number_dict)            
        if almost_number_is_empty_dict:
            almost_number_is_empty_dict = json.loads(almost_number_is_empty_dict)        
        if type_pair:
            type_pair = json.loads(type_pair)
            
        caller = path.get_caller(request)        
        file_path = path.get_upload_root(request, caller=caller)
        
        try:
            if interval_dict:
                interval_dict = json.loads(interval_dict)
            parser.create_DPView_json_file(file_path, file_name,pair_dict,
                type_pair=type_pair,
                interval_dict=interval_dict,
                almost_number_dict=almost_number_dict,
                almost_number_is_empty_dict=almost_number_is_empty_dict,)
        except Exception as e:
            logging.critical(username + ' ParserView run fail', exc_info=True)
            JsonResponse({"message":gettext("程式執行失敗，請稍後再試，若多次執行失敗，請聯絡服務人員為您服務")}, status=404)
        else:
            logging.info(username + ' ParserView run success')
            return HttpResponse(status=204)
        logging.critical(username + ' unknown error', exc_info=True)
        return JsonResponse({"message":gettext("有尚未捕捉到的例外，請回報服務人員，謝謝")}, status=404)
        
class CustomView(View):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):        
        file_name = kwargs.get('csv_name')
        if not file_name:
            return redirect('home')
         
        request_dict = self.get_request_dict(request, *arg, **kwargs)
        return render(request, 'general/parameter_custom.html', request_dict)
        
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        file_name = kwargs.get('csv_name')
        if not file_name:
            return redirect('home')
            
        title_id_pair = request.POST.get('title_id_pair', None)
        interval_dict = request.POST.get('interval_dict', None)
        structure_dict = request.POST.get('structure_dict', None)
        almost_number_is_empty_dict = request.POST.get('almost_number_is_empty_dict', None)
        request_dict = self.get_request_dict(request, *arg, **kwargs)
        request_dict['title_id_pair'] = title_id_pair
        request_dict['interval_dict'] = interval_dict
        request_dict['structure_dict'] = structure_dict
        request_dict['almost_number_is_empty_dict'] = almost_number_is_empty_dict
        return render(request, 'general/parameter_custom.html', request_dict)
    
    def get_request_dict(self, request, *arg, **kwargs):
        parser = JsonParser()
        path = Path()
        
        string_element_dict = {} # column_title - element        
        file_name = kwargs.get('csv_name')            
        caller = path.get_caller(request)
            
        file_path = path.get_upload_path(request, file_name, caller=caller)
        data_frame = DataframeDetection(file_path)
        string_element_dict = data_frame.get_file_string_element(almost_number_filter=False)
              
        request_dict = {}  
        request_dict = self.set_url_path(request_dict, caller, file_name)
        request_dict['string_element_dict'] = string_element_dict
        request_dict['caller'] = caller
        request_dict['file_name'] = file_name
        request_dict['custom_mode'] = 'json_parser'
        return request_dict
    
    def set_url_path(self, request_dict, caller, file_name):
        request_dict['create_json'] = reverse(caller+':create_json')
        request_dict['title_check'] = reverse(caller+':title_check')
        request_dict['advanced_settings_url'] = reverse(caller+':advanced_settings', args=[file_name])
        request_dict['base_settings_url'] = reverse(caller+':custom')+file_name+'/'
        request_dict['previous_page_url'] = reverse(caller+':home')
        request_dict['execute_url'] = reverse(caller+':execute_page', args=[file_name])
        request_dict['upload_display_url'] = reverse(caller+':display', args=['upload'])
        return request_dict

class AdvancedSettingsView(CustomView):
    @method_decorator(login_required)
    def get(self, request, *arg, **kwargs):
        file_name = kwargs.get('csv_name')
        if not file_name:
            return redirect('home')
            
        request_dict = self.get_request_dict(request, *arg, **kwargs)
        return render(request, 'general/parameter_custom.html', request_dict)
    
    @method_decorator(login_required)
    def post(self, request, *arg, **kwargs):
        file_name = kwargs.get('csv_name')
        if not file_name:
            return redirect('home')
            
        title_id_pair = request.POST.get('title_id_pair', None)
        interval_dict = request.POST.get('interval_dict', None)
        structure_dict = request.POST.get('structure_dict', None)
        almost_number_is_empty_dict = request.POST.get('almost_number_is_empty_dict', None)
        request_dict = self.get_request_dict(request, *arg, **kwargs)
        request_dict['title_id_pair'] = title_id_pair
        request_dict['interval_dict'] = interval_dict
        request_dict['structure_dict'] = structure_dict
        request_dict['almost_number_is_empty_dict'] = almost_number_is_empty_dict
        return render(request, 'general/parameter_custom.html', request_dict)
        
    def get_request_dict(self, request, *arg, **kwargs):
        path = Path()
        
        file_name = kwargs.get('csv_name')            
        caller = path.get_caller(request) 
        
        file_path = path.get_upload_path(request, file_name, caller=caller)
        data_frame = DataframeDetection(file_path)
        type_pair = data_frame.get_type_pair()
        number_title_list = data_frame.get_number_title(type_pair=type_pair)
        number_type_pair = data_frame.get_number_type_pair(number_title_list, type_pair=type_pair)
        max_value_dict, min_value_dict = data_frame.get_number_limit(number_title_list, number_type_pair=number_type_pair)
           
        request_dict = super().get_request_dict(request, *arg, **kwargs)
        request_dict['type_pair'] = type_pair
        request_dict['advanced_settings'] = True
        request_dict['number_title_list'] = number_title_list
        request_dict['number_type_pair'] = number_type_pair
        request_dict['max_value_dict'] = max_value_dict
        request_dict['min_value_dict'] = min_value_dict
        return request_dict