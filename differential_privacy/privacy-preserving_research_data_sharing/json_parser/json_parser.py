# -*- coding: UTF-8 -*-

import json
import math
import re
import pandas as pd
from django.utils.translation import gettext
from general.exception import NotAddressException
from general.function import ContentDetection
from general.function import DataframeDetection

class JsonParser():

    __n_parts = 10
    __float_accuracy = 4
    __tw_address_accuracy_pattern = '縣市鄉鎮市區街路村里巷弄號樓室'
    
    def get_interval(self, number_list, column_type=None):
        detection = ContentDetection()
        if column_type == 'str' or column_type == 'almost_number' or not detection.is_number(number_list):
            raise TypeError(str(number_list) + ' is not number list')
        number_list = list(filter(None, number_list))
        if column_type == 'float':
            number_list_is_float = True
        elif column_type == 'int':
            number_list_is_float = False
        else:
            number_list_is_float = detection.is_float(number_list)
        if number_list_is_float:
            min_value = float(min(number_list))
            max_value = float(max(number_list))
        else:
            min_value = int(min(number_list))
            max_value = int(max(number_list))
        interval = []
        gap = (max_value - min_value) / self.__n_parts
        if number_list_is_float:
            for i in range(self.__n_parts):
                upper_limit = round(min_value + gap*(i+1), self.__float_accuracy)
                lower_limit = round(min_value + gap*i, self.__float_accuracy)
                interval.append([lower_limit, upper_limit])
        else:
            for i in range(self.__n_parts):
                upper_limit = round(min_value + gap*(i+1))
                lower_limit = round(min_value + gap*i)
                interval.append([lower_limit, upper_limit])
        return interval
        
    def get_unrelated_structure(self, string_list, ancestor):
        genealogy = {}
        for item in string_list:
            genealogy[item] = ancestor
        genealogy[ancestor] = ancestor
        return genealogy
        
    def get_tw_address_structure(self, address_list):
        genealogy = {}
        for address in address_list:
            split_list = self.split_tw_address(address)
            key = ''
            temp = ''
            for token in split_list:
                key = key + token
                if temp:
                    genealogy[key] = temp
                else:
                    genealogy[key] = token
                temp = key
        return genealogy
        
    def split_tw_address(self, address):
        pattern = '[^'+self.__tw_address_accuracy_pattern+']*'+\
                    '['+self.__tw_address_accuracy_pattern+']'
        token_list = re.findall(pattern, address)
        return token_list
        
    def get_us_address_structure(self, address_list):
        genealogy = {}
        for address in address_list:
            token_list = re.split(',\s?', address)
            key = ''
            temp = ''
            for token in reversed(token_list):
                key = token + key
                if temp:
                    genealogy[key] = temp
                else:
                    city = re.split('\s',key)[0]
                    genealogy[city] = city
                    genealogy[key] = city
                temp = key
                key = ', ' + key
        return genealogy
    
    def parser_to_json(self, file_path, structure, type_pair=None, interval_dict=None):
        json_dict = {}
        detection = ContentDetection()
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        if not type_pair:
            data_frame = DataframeDetection(file_path)
            type_pair = data_frame.get_type_pair()
        for column_title in dataframe:
            temp = {}
            column = dataframe.loc[:, column_title].values.tolist()
            if type_pair[column_title] == 'str' or detection.is_string(column):
                temp['type'] = 'categorical'
                temp['structure'] = structure[column_title]
            elif (type_pair[column_title] == 'float' or type_pair[column_title] == 'int') or detection.is_number(column):
                temp['type'] = 'numerical'
                temp['min'] = min(column)
                temp['max'] = max(column)
                
                if type_pair[column_title] == 'float' or detection.is_float(column):
                    temp['num_type'] = 'float'
                else:
                    temp['num_type'] = 'int'
                
                if interval_dict and column_title in interval_dict:
                    interval = []
                    value_list = interval_dict[column_title]
                    for i in range(len(value_list)-1):
                        interval.append([value_list[i], value_list[i+1]])
                    temp['interval'] = interval
                else:
                    if type_pair:
                        temp['interval'] = self.get_interval(column, column_type=type_pair[column_title])
                    else:
                        temp['interval'] = self.get_interval(column)            
            else:
                temp['type'] = 'categorical'
                temp['structure'] = {'':''}
            json_dict[column_title] = temp
        return json_dict
    
    def parser_to_DPView_json(self, file_path, pair_dict, type_pair=None, interval_dict=None, almost_number_dict=None, almost_number_is_empty_dict=None):
        json_dict = {}
        detection = ContentDetection()
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        if not type_pair:
            data_frame = DataframeDetection(file_path)
            type_pair = data_frame.get_type_pair()
        for column_title in dataframe:
            temp = {}
            column = dataframe.loc[:, column_title].values.tolist()
            if (type_pair[column_title] == 'str' or detection.is_string(column)) and type_pair[column_title] != 'almost_number':
                temp['type'] = 'cat'
            elif (type_pair[column_title] == 'float' or type_pair[column_title] == 'int') or detection.is_number(column):
                if pair_dict[column_title] == 'number':
                    temp['type'] = 'num'
                elif pair_dict[column_title] == 'single':
                    temp['type'] = 'single'
                elif pair_dict[column_title] == 'category':
                    temp['type'] = 'num2cat'
                if interval_dict and column_title in interval_dict:
                    interval = []
                    value_list = interval_dict[column_title]
                    for i in range(len(value_list)-1):
                        interval.append([value_list[i], value_list[i+1]])
                    temp['bucket'] = interval
                else:
                    if type_pair:
                        temp['bucket'] = self.get_interval(column, column_type=type_pair[column_title])
                    else:
                        temp['bucket'] = self.get_interval(column)
            elif type_pair[column_title] == 'almost_number' or detection.almost_is_number(column):
                if almost_number_is_empty_dict and column_title in almost_number_is_empty_dict:
                    dataframe.loc[:, column_title] = dataframe.loc[:, column_title].replace(almost_number_is_empty_dict[column_title], '')
                    if almost_number_is_empty_dict[column_title] == almost_number_dict[column_title]:
                        column = dataframe.loc[:, column_title].values.tolist()
                        temp['type'] = 'num'
                        temp['bucket'] = self.get_interval(column)
                    else:
                        temp['type'] = 'cat'
                    print(temp['type'])
                else:
                    temp['type'] = 'cat'
            else:
                temp['type'] = 'single'
            json_dict[column_title] = temp
        dataframe.to_csv(file_path, index=False)
        return json_dict
        
    def create_json_file(self, file_path, file_name, structure_mode, structure_dict, type_pair=None, interval_dict=None):
        for key in structure_mode:            
            mode = structure_mode[key]
            if mode == 'tw_address':
                structure_dict[key] = \
                    self.get_tw_address_structure(structure_dict[key].keys())
                if not structure_dict[key]:
                    raise NotAddressException(key + gettext("欄位所存資料並非地址，請重新填寫"))
            elif mode == 'us_address':
                structure_dict[key] = \
                    self.get_us_address_structure(structure_dict[key].keys())
                if not structure_dict[key]:
                    raise NotAddressException(key + gettext("欄位所存資料並非地址，請重新填寫"))
            elif mode == 'unrelated':
                structure_dict[key] = \
                    self.get_unrelated_structure(structure_dict[key].keys(), key)
            if not structure_dict[key]:
                raise Exception(key + gettext("欄位所生成的配對資料為空，請聯絡開發人員排除問題"))
        directory_name = file_name.split(".")[-2]
        file_path = file_path + directory_name + '/'
        json_path = file_path + directory_name + '_dict.json'
        json_object = json.dumps(self.parser_to_json\
                (file_path+file_name, structure_dict,
                type_pair=type_pair,
                interval_dict=interval_dict,))
        with open(json_path, 'w') as file:
            file.write(json_object)
            
    def create_DPView_json_file(self, file_path, file_name, pair_dict, type_pair=None, interval_dict=None, almost_number_dict=None, almost_number_is_empty_dict=None):
        directory_name = file_name.split(".")[-2]
        file_path = file_path + directory_name + '/'
        json_path = file_path + directory_name + '_dict.json'
        json_object = json.dumps(self.parser_to_DPView_json\
                (file_path+file_name, pair_dict,
                type_pair=type_pair,
                interval_dict=interval_dict,
                almost_number_dict=almost_number_dict,
                almost_number_is_empty_dict=almost_number_is_empty_dict,))
        with open(json_path, 'w') as file:
            file.write(json_object)