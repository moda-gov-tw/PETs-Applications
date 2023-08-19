import pandas as pd
from django.conf import settings
from django.utils.html import escape
from general.models import ExecuteModel

class Path():        
    def get_caller(self, request):
        try:
            username = request.user.get_username()
            file = ExecuteModel.objects.get(user_name=username)
            return file.caller
        except Exception as e:
            if request.resolver_match.app_names:
                caller = request.resolver_match.app_names[0] # get app_names
            return caller
        
    def get_output_path(self, request, file_name, caller=None):
        directory_name = file_name.split(".")[-2]
        return self.get_output_directory(request, file_name, caller=caller)\
                +directory_name+'_output.csv'
        
    def get_output_directory(self, request, file_name, caller=None):
        file_root = self.get_output_root(request, caller)
        directory_name = file_name.split(".")[-2]
        return file_root+directory_name+'/'
        
    def get_upload_path(self, request, file_name, caller=None):
        return self.get_upload_directory(request, file_name, caller=caller)+file_name
        
    def get_upload_directory(self, request, file_name, caller=None):
        file_root = self.get_upload_root(request, caller)
        directory_name = file_name.split(".")[-2]
        return file_root+directory_name+'/'
        
    def get_output_root(self, request, caller=None):
        return self._get_root('output', request, caller=caller)
    
    def get_upload_root(self, request, caller=None):
        return self._get_root('upload', request, caller=caller)
        
    def _get_root(self, mode, request, caller=None):
        if mode == 'upload':
            root = settings.UPLOAD_ROOT
        elif mode == 'output':
            root = settings.OUTPUT_ROOT
        if not caller:
            caller = self.get_caller(request)
        username = request.user.get_username()
        return root+caller+'/'+username+'/'

class ContentDetection():
    def is_string(self, item_list):
        if not item_list:
            return False
        for item in item_list:
            if not item:
                continue
            try:
                float(item)
            except ValueError:
                return True
        return False
        
    def is_number(self, item_list):
        if not item_list:
            return False
        is_empty = True
        for item in item_list:
            if not item:
                continue
            try:
                float(item)
                is_empty = False
            except ValueError:
                return False
        if is_empty:
            return False
        return True
    
    def almost_is_number(self, item_list):
        if not item_list:
            return False
        str_set = set()
        have_number = False
        for item in item_list:
            if not item:
                continue
            try:
                float(item)
                have_number = True
            except ValueError:
                str_set.add(item)
        if have_number:
            if len(str_set) <= 3 and len(str_set) != 0:
                return True
        return False
        
    def is_float(self, item_list):
        if not self.is_number(item_list):
            return False
        for item in item_list:
            if not item:
                continue
            if type(item) is float:
                return True
            if type(item) is str and item.find('.') != -1:
                return True
        return False

class DataframeDetection():
    def __init__(self, file_path):
        self.dataframe = pd.read_csv(file_path, keep_default_na=False)
        self.detection = ContentDetection()
    
    def get_number_title(self, type_pair=None):
        number_title_list = []
        for column_title in self.dataframe:
            if type_pair:
                if type_pair[column_title] == 'float' or type_pair[column_title] == 'int':
                    number_title_list.append(column_title)
            else:
                if self.detection.is_number(self.dataframe.loc[:, column_title].values.tolist()):
                    number_title_list.append(column_title)
        return number_title_list
        
    def get_number_limit(self, number_title_list, number_type_pair=None):
        max_value_dict = {}
        min_value_dict = {}
        for number_title in number_title_list:
            data = self.dataframe.loc[:, number_title].values.tolist()
            data = list(filter(None, data))
            if number_type_pair:
                if(number_type_pair[number_title] == 'float'):
                    max_value_dict[number_title] = float(max(data))
                    min_value_dict[number_title] = float(min(data))
                elif(number_type_pair[number_title] == 'int'):
                    max_value_dict[number_title] = int(max(data))
                    min_value_dict[number_title] = int(min(data))
                else:
                    raise Exception('number_type_pair error')
            else:
                if self.detection.is_float(self.dataframe.loc[:, number_title].values.tolist()):
                    max_value_dict[number_title] = float(max(data))
                    min_value_dict[number_title] = float(min(data))
                else:
                    max_value_dict[number_title] = int(max(data))
                    min_value_dict[number_title] = int(min(data))
        return max_value_dict, min_value_dict
        
    def get_number_type_pair(self, number_title_list, type_pair=None):
        number_type_pair = {}
        for number_title in number_title_list:
            if type_pair:
                number_type_pair[number_title] = type_pair[number_title]
            else:
                data = self.dataframe.loc[:, number_title].values.tolist()
                data = list(filter(None, data))
                if self.detection.is_float(self.dataframe.loc[:, number_title].values.tolist()):
                    number_type_pair[number_title] = 'float'
                else:
                    number_type_pair[number_title] = 'int'
        return number_type_pair
        
    def get_type_pair(self):
        type_pair = {}
        for column_title in self.dataframe:
            column = self.dataframe.loc[:, column_title].values.tolist()
            
            is_empty = True
            for item in column:
                if not item:
                    continue
                is_empty = False
                break
                
            if is_empty:
                type_pair[column_title] = 'empty'
                continue
                
            if self.detection.is_string(column):
                if self.detection.almost_is_number(column):
                    type_pair[column_title] = 'almost_number'
                else:
                    type_pair[column_title] = 'str'
            else:
                if self.detection.is_float(column):
                    type_pair[column_title] = 'float'
                else:
                    type_pair[column_title] = 'int'
        return type_pair
        
    def get_file_string_element(self, almost_number_filter=True, type_pair=None):
        if almost_number_filter:
            if type_pair:
                column_element = self.get_column_element(target='str', type_pair=type_pair)
            else:
                column_element = self.get_column_element(target='str')
        else:
            if type_pair:
                column_element = self.get_column_element(target='all_str', type_pair=type_pair)
            else:
                column_element = self.get_column_element(target='all_str')
        return column_element
    
    def get_almost_number_element(self, type_pair=None):
        if type_pair:
            column_element = self.get_column_element(target='almost_number', type_pair=type_pair)
        else:
            column_element = self.get_column_element(target='almost_number')
        return column_element
                
    def get_column_element(self, target, type_pair=None):
        column_element = {}
        for column_title in self.dataframe:
            column = self.dataframe.loc[:, column_title].values.tolist()
            
            if target == 'all_str':
                if type_pair and (type_pair[column_title] == 'str' or type_pair[column_title] == 'almost_number'):
                    column_element[column_title] = list(filter(None, list(set(column))))
                if(self.detection.is_string(column)):
                    column_element[column_title] = list(filter(None, list(set(column))))
            elif target == 'str':
                if type_pair and type_pair[column_title] == 'str':
                    column_element[column_title] = list(filter(None, list(set(column))))
                if(self.detection.is_string(column) and not self.detection.almost_is_number(column)):
                    column_element[column_title] = list(filter(None, list(set(column))))
            elif target == 'almost_number':
                if type_pair and type_pair[column_title] == 'almost_number' or self.detection.almost_is_number(column):
                    remove_empty = list(filter(None, list(set(column))))
                    temp = set()
                    for item in remove_empty:
                        try:
                            float(item)
                        except ValueError:
                            temp.add(item)
                    column_element[column_title] = list(temp)
        return column_element