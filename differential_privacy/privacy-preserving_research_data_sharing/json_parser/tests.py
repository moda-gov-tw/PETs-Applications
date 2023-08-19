# -*- coding: UTF-8 -*-

from json_parser.json_parser import JsonParser

import unittest
import json
import csv
import os
import pandas as pd

class TestParser(unittest.TestCase):
    
    csv_path = 'test.csv'
    json_parser = JsonParser()
    
    @classmethod
    def setUpClass(cls):
        with open(cls.csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['String','Integer','String2','Float','String3'])
            writer.writerow(['a','1','x','1.1','a x'])
            writer.writerow(['b','22','y','22.22','b/y'])
            writer.writerow(['c','333','x','333.333','c-z'])
            
        cls.df = pd.read_csv(cls.csv_path)
        cls.categorical = cls.df.loc[:, 'String'].values.tolist()
        cls.number_int = cls.df.loc[:, 'Integer'].values.tolist()
        cls.number_float = cls.df.loc[:, 'Float'].values.tolist()
        cls.mixing = ['a',2,'c',4,'d']
        cls.empty = []
       
    @classmethod       
    def tearDownClass(cls):
        try:
            os.remove(cls.csv_path)
        except OSError as e:
            print(e)
        else:
            print("Test file is deleted successfully")
    
    def test_calculate_interval(self):
        number_int_interval = self.json_parser.get_interval(self.number_int)
        number_float_interval = self.json_parser.get_interval(self.number_float)
        
        test_int_interval = [[1,34],[34,67],\
                            [67,101],[101,134],\
                            [134,167],[167,200],\
                            [200,233],[233,267],\
                            [267,300],[300,333]]
        
        test_float_interval = [[1.1,34.3233],[34.3233,67.5466],\
                                [67.5466,100.7699],[100.7699,133.9932],\
                                [133.9932,167.2165],[167.2165,200.4398],\
                                [200.4398,233.6631],[233.6631,266.8864],\
                                [266.8864,300.1097],[300.1097,333.333]]
        
        interval_quantity = len(number_int_interval)
        self.assertEqual(interval_quantity, len(test_int_interval))
        for i in range(interval_quantity):
            self.assertEqual(len(number_int_interval[i]), 2)
            for j in range(2):
                self.assertEqual\
                    (number_int_interval[i][j], test_int_interval[i][j])
        
        interval_quantity = len(number_float_interval)
        self.assertEqual(interval_quantity, len(test_float_interval))
        for i in range(interval_quantity):
            self.assertEqual(len(number_int_interval[i]), 2)
            for j in range(2):
                self.assertAlmostEqual\
                    (number_float_interval[i][j], test_float_interval[i][j])
                    
        with self.assertRaises(Exception):
            self.json_parser.get_interval(self.categorical)
            self.json_parser.get_interval(self.mixing)
            self.json_parser.get_interval(self.empty)
    
    def test_unrelated_structure(self):
        test_structure = {'String':'String', 'a':'String', 'b':'String', 'c':'String'}
        structure = self.json_parser.get_unrelated_structure(self.categorical, 'String')
        
        key_list = structure.keys()
        self.assertEqual(len(key_list), len(test_structure.keys()))
        for key in key_list:
            self.assertEqual(structure.get(key), test_structure.get(key))
        
    def test_tw_address_structure(self):
        test_structure = {'台北市大安區忠孝東路100號':'台北市大安區忠孝東路',\
                        '台中市清水區護岸路123號':'台中市清水區護岸路',\
                        '台中市南區學府路16號':'台中市南區學府路',\
                        '台北市大安區忠孝東路':'台北市大安區',\
                        '台中市清水區護岸路':'台中市清水區',\
                        '台中市南區學府路':'台中市南區',\
                        '台北市大安區':'台北市',\
                        '台中市清水區':'台中市',\
                        '台中市南區':'台中市',\
                        '台北市':'台北市',\
                        '台中市':'台中市'}
                        
        address_list = ['台北市大安區忠孝東路100號',\
                        '台中市清水區護岸路123號',\
                        '台中市南區學府路16號']
                        
        structure = self.json_parser.get_tw_address_structure(address_list)
        key_list = structure.keys()
        self.assertEqual(len(key_list), len(test_structure.keys()))
        for key in key_list:
            self.assertEqual(structure.get(key), test_structure.get(key))

    def test_us_address_structure(self):
        test_structure = {'678 Montgomery St, Jersey City, NJ 07306':'Jersey City, NJ 07306',\
                        '30 Mall Dr W, Jersey City, NJ 07310':'Jersey City, NJ 07310',\
                        '75 Grasslands Rd, Valhalla, NY 10595':'Valhalla, NY 10595',\
                        'Jersey City, NJ 07306':'NJ 07306',\
                        'Jersey City, NJ 07310':'NJ 07310',\
                        'Valhalla, NY 10595':'NY 10595',\
                        'NJ 07306':'NJ',\
                        'NJ 07310':'NJ',\
                        'NY 10595':'NY',\
                        'NJ':'NJ',\
                        'NY':'NY'}
                        
        address_list = ['678 Montgomery St, Jersey City, NJ 07306',\
                        '30 Mall Dr W, Jersey City, NJ 07310',\
                        '75 Grasslands Rd, Valhalla, NY 10595']
                        
        structure = self.json_parser.get_us_address_structure(address_list)
        key_list = structure.keys()
        self.assertEqual(len(key_list), len(test_structure.keys()))
        for key in key_list:
            self.assertEqual(structure.get(key), test_structure.get(key))
    
    def test_split_tw_address(self):
        test_split = [['台北市','大安區','忠孝東路','100號'],\
                        ['台中市','清水區','護岸路','123號'],\
                        ['台中市','南區','學府路','16號']]
                        
        address_list = ['台北市大安區忠孝東路100號',\
                        '台中市清水區護岸路123號',\
                        '台中市南區學府路16號']
        split_list = []
        for address in address_list:
            split_list.append(self.json_parser.split_tw_address(address))
        
        address_quantity = len(split_list)
        self.assertEqual(address_quantity, len(test_split))
        for i in range(address_quantity):
            token_quantity = len(split_list[i])
            self.assertEqual(token_quantity, len(test_split[i]))
            for j in range(token_quantity):
                self.assertEqual(split_list[i][j], test_split[i][j])
    
    def test_get_file_string_element(self):
        test_element = {'String':{'a','b','c'},\
                        'String2':{'x','y'},\
                        'String3':{'a x','b/y','c-z'}}
        file_string_element = self.json_parser.get_file_string_element(self.csv_path)
        key_list = file_string_element.keys()
        self.assertEqual(len(key_list), len(test_element.keys()))
        for column_name in key_list:
            self.assertEqual(set(file_string_element[column_name]),\
                                test_element[column_name])
        
    def test_get_column_element(self):
        column = ['a','r','d','a','d']
        test_element = {'a','r','d'}
        element = self.json_parser.get_column_element(column)
        self.assertEqual(set(element), test_element)
    
    def test_parser_to_json(self):
        test_json = {
                        'String':{
                            'type':'categorical',
                            'structure':{
                                'String':'String',
                                'a':'String',
                                'b':'String',
                                'c':'String'
                            }
                        },
                        'Integer':{
                            'type':'numerical', 
                            'min':1, 
                            'max':333, 
                            'num_type':'int',
                            'interval':[[1,34],[34,67],\
                            [67,101],[101,134],\
                            [134,167],[167,200],\
                            [200,233],[233,267],\
                            [267,300],[300,333]]
                        },
                        'String2':{
                            'type':'categorical',
                            'structure':{
                                'x':'x',
                                'y':'x'
                            }
                        },
                        'Float':{
                            'type':'numerical', 
                            'min':1.1, 
                            'max':333.333, 
                            'num_type':'float',
                            'interval':[[1.1,34.3233],[34.3233,67.5466],\
                                [67.5466,100.7699],[100.7699,133.9932],\
                                [133.9932,167.2165],[167.2165,200.4398],\
                                [200.4398,233.6631],[233.6631,266.8864],\
                                [266.8864,300.1097],[300.1097,333.333]]
                        },
                        'String3':{
                            'type':'categorical',
                            'structure':{
                                'a x':'x',
                                'b/y':'x',
                                'c-z':'x'
                            }
                        }
                    }
        test_json_string = json.dumps(test_json)
        structure = {
                        'String':{
                            'String':'String',
                            'a':'String',
                            'b':'String',
                            'c':'String'
                        },
                        'String2':{
                            'x':'x',
                            'y':'x'
                        },
                        'String3':{
                            'a x':'x',
                            'b/y':'x',
                            'c-z':'x'
                        },
                    }
        json_string = json.dumps(self.json_parser.parser_to_json\
                                (self.csv_path, structure))
        
        self.assertEqual(test_json_string, json_string)
    
if __name__ == '__main__':
    unittest.main()
