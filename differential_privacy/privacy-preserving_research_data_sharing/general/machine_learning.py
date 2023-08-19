from sklearn import tree
from sklearn import ensemble
from sklearn import svm
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle
import pandas as pd

class MachineLearning():
    SUPPORT_LIST = ['decision_trees', 'svm', 'random_forest']
    
    train_percent = 80
    train_feature = None
    test_feature = None
    train_label = None
    test_label = None
    
    def __init__(self, method, mode, train_file_path, test_file_path):
        if method == 'decision_trees':
            if mode == 'classification':
                self.method_object = tree.DecisionTreeClassifier()
            elif mode == 'regression':
                self.method_object = tree.DecisionTreeRegressor()
            else:
                raise AttributeError(method + " 無此mode：" + mode)
        elif method == 'svm':
            if mode == 'classification':
                self.method_object = svm.SVC()
            elif mode == 'regression':
                self.method_object = svm.SVR()
            else:
                raise AttributeError(method + " 無此mode：" + mode)            
        elif method == 'random_forest':
            if mode == 'classification':
                self.method_object = ensemble.RandomForestClassifier(max_depth=20, random_state=0)
            elif mode == 'regression':
                self.method_object = ensemble.RandomForestRegressor(max_depth=20, random_state=0)
            else:
                raise AttributeError(method + " 無此mode：" + mode)
        else:
            raise AttributeError("無此method：" + method)
        self.preprocessing(train_file_path, test_file_path)

    def preprocessing(self, train_file_path, test_file_path):
        train_feature, train_label = self.getDataset(train_file_path)
        test_feature, test_label = self.getDataset(test_file_path)
        
        train_feature, test_feature = self.one_hot_encoding(train_feature, test_feature)
                
        split_point = len(train_feature)*self.train_percent//100        
        self.train_feature = train_feature[0:split_point]
        self.train_label = train_label[0:split_point]
        
        split_point = len(test_feature)*self.train_percent//100
        self.test_feature = test_feature[split_point:]
        self.test_label = test_label[split_point:]
    
    def fit(self):
        self.method_object.fit(self.train_feature, self.train_label)
        
    def predict(self, feature):
        return self.method_object.predict(feature)
        
    def score(self):
        accuracy = self.method_object.score(self.test_feature, self.test_label)
        return accuracy
        
    def get_mse(self):
        predict_label = self.method_object.predict(self.test_feature)
        return mean_squared_error(self.test_label, predict_label)
    
    def getDataset(self, file_path):
        dataframe = pd.read_csv(file_path, encoding='utf-8', keep_default_na=False)
        dataframe = shuffle(dataframe)
        feature = dataframe.iloc[:, 0:-1]
        label = dataframe.iloc[:, [-1]].values.tolist()
        return feature, label
        
    def one_hot_encoding(self, dataframe1, dataframe2):
        encoding_dict, delete_list = self.get_encoding_dict(dataframe1, dataframe2)
        list1 = self.encoding(dataframe1, encoding_dict, delete_list)
        list2 = self.encoding(dataframe2, encoding_dict, delete_list)
        return list1, list2
            
    def need_one_hot(self, data):
        if type(data) is str or type(data) is chr:
            return True
        return False

    def get_elements(self, check_data, dataframe):
        if type(check_data) is str or type(check_data) is chr:
            return set(dataframe.values.tolist())
        else:
            return set()
    
    def get_encoding_dict(self, dataframe1, dataframe2):
        encoding_dict = {}
        delete_list = []
        dataframe1_set_dict = {}
        dataframe2_set_dict = {}
        
        for column_title in dataframe1:
            data1 = None
            i = 0
            while not data1 and i < dataframe1.shape[0]:
                if not data1:
                    data1 = dataframe1.loc[i, column_title]
                i = i + 1
            if self.need_one_hot(data1):
                dataframe1_set_dict[column_title] = self.get_elements(data1, dataframe1.loc[:, column_title])
        
        for column_title in dataframe2:
            data2 = None
            i = 0
            while not data2 and i < dataframe2.shape[0]:
                if not data2:
                    data2 = dataframe2.loc[i, column_title]
                i = i + 1
            if self.need_one_hot(data2):
                dataframe2_set_dict[column_title] = self.get_elements(data2, dataframe2.loc[:, column_title])
                
        for column_title in dataframe1_set_dict:
            elements1 = dataframe1_set_dict[column_title]
            if column_title in dataframe2_set_dict:
                elements2 = dataframe2_set_dict[column_title]
                encoding_dict[column_title] = list(elements1.union(elements2))
        delete_list = list((set(dataframe1_set_dict.keys()) | set(dataframe2_set_dict.keys())) - set(encoding_dict.keys()))
        return encoding_dict, delete_list
        
    def encoding(self, dataframe, encoding_dict, delete_list):
        encoding_list = []
        for row in range(dataframe.shape[0]):
            column_list = []
            for column_title in dataframe:
                if column_title in delete_list:
                    continue
                data = dataframe.loc[row, column_title]
                if column_title in encoding_dict:
                    if data not in encoding_dict[column_title]:
                        data = self.number_pair(data, encoding_dict[column_title])
                    for element in encoding_dict[column_title]:
                        if data == element:
                            column_list.append(1)
                        else:
                            column_list.append(0)
                else:
                    column_list.append(data)
            encoding_list.append(column_list.copy())
        return encoding_list
    
    def number_pair(self, number, interval_set):
        for interval in interval_set:
            limit = interval.split('-')
            min = float(limit[0])
            max = float(limit[1])
            if number > min and number < max:
                return interval