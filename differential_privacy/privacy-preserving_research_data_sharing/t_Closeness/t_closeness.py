#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import math
import json
import os

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.utils.translation import gettext

from general.exception import BreakProgramException, ParameterException
from general.models import ExecuteModel

import logging
from datetime import date 
today = date.today()
logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename= str(today) +'_log.txt')

def show_progress(request):
    try:
        username = request.user.get_username()
        file = ExecuteModel.objects.get(user_name=username)
        data = {
            'log':file.log,
            'num_progress':file.num_progress,
        }
        return JsonResponse(data, safe=False)
    except:
        data = {
            'log':gettext('程式已被取消執行，請重新嘗試執行'),
            'num_progress':0,
        }
        return JsonResponse(data, safe=False)
    
def break_program(file):
    file.skip = True
    file.save()
        
def run(request):
    username = request.user.get_username()
    file = ExecuteModel.objects.get(user_name=username)
    
    file_name = str(request.GET.get('csv_name',None))
    directory_name = file_name.split(".")[-2]
    username = request.user.get_username()
    dict_file_name = settings.UPLOAD_ROOT + 't_Closeness/' + username + '/' + directory_name + '/' + directory_name + '_dict.json'
    progress_count = 0
    file.num_progress = 5
    file.log = 'Building data information...'
    logging.info('t_Closeness Building data information...')
    file.save()
    if file.skip:
        raise BreakProgramException(gettext('程式成功終止'))
    k = int(request.GET.get('k', None))
    t = float(request.GET.get('t', 100000))
    df_data = pd.read_csv(settings.UPLOAD_ROOT + 't_Closeness/' + username + '/' + directory_name + '/' + file_name, keep_default_na=False)
    record_num = df_data.shape[0]
    attr_num = df_data.shape[1]
    column_name = list(df_data.columns)
    for attr_id in range(attr_num):
        if file.skip:
            raise BreakProgramException(gettext('程式成功終止'))
    sa_id = attr_num - 1
    qi_list = []
    for attr_id in range(attr_num):
        if attr_id != sa_id:
            qi_list.append(attr_id)
    qi_num = len(qi_list)
    
    with open(dict_file_name) as json_file:
        data_dict = json.load(json_file)
    for attr_id in qi_list:
        if data_dict[column_name[attr_id]]['type'] == 'categorical':
            category_ancestor_dict = {}
            for category in data_dict[column_name[attr_id]]['structure'].keys():
                ancestor_set = set()
                ancestor_set.add(category)
                current_category = category
                while True:
                    if file.skip:
                        raise BreakProgramException(gettext('程式成功終止'))
                    father_category = data_dict[column_name[attr_id]]['structure'][current_category]
                    if father_category == current_category:
                        break
                    current_category = father_category
                    ancestor_set.add(current_category)
                category_ancestor_dict[category] = ancestor_set
            category_distance_dict = {}
            category_generalize_dict = {}
            for category_1 in data_dict[column_name[attr_id]]['structure'].keys():
                for category_2 in data_dict[column_name[attr_id]]['structure'].keys():
                    # Calculate distance
                    union_len = len(category_ancestor_dict[category_1].union(category_ancestor_dict[category_2]))
                    intersection_len = len(category_ancestor_dict[category_1].intersection(category_ancestor_dict[category_2]))
                    distance = math.log(1 + (union_len - intersection_len) / union_len, 2)
                    category_distance_dict[(category_1, category_2)] = distance
                    # Match generalized result
                    current_category = category_2
                    while True:
                        if file.skip:
                            raise BreakProgramException(gettext('程式成功終止'))
                        if current_category in category_ancestor_dict[category_1]:
                            category_generalize_dict[(category_1, category_2)] = current_category
                            break
                        current_category = data_dict[column_name[attr_id]]['structure'][current_category]
            data_dict[column_name[attr_id]]['category_distance'] = category_distance_dict
            data_dict[column_name[attr_id]]['category_generalize'] = category_generalize_dict
    original_data = []
    for row in range(record_num):
        data_buffer = []
        for col in range(attr_num):
            data_buffer.append(df_data.iloc[row, col])
        original_data.append(data_buffer)
    # In[ ]:
    def KLD(P, Q):
        if file.skip:
            raise BreakProgramException(gettext('程式成功終止'))
        buffer = np.log(P / Q)
        buffer[buffer==np.inf] = 1000000
        return np.sum(P * buffer)
    
    def person_distance(p1, p2):
        if file.skip:
            raise BreakProgramException(gettext('程式成功終止'))
        diff = 0
        for attr_id in qi_list:
            if data_dict[column_name[attr_id]]['type'] == 'numerical':
                diff += abs(p1[attr_id] - p2[attr_id]) / (data_dict[column_name[attr_id]]['max'] - data_dict[column_name[attr_id]]['min'])
            elif data_dict[column_name[attr_id]]['type'] == 'categorical':
                diff += data_dict[column_name[attr_id]]['category_distance'][(p1[attr_id], p2[attr_id])]
        diff /= qi_num
        return diff
        
    def merge_k_anony(cluster_1, cluster_2):
        if file.skip:
            raise BreakProgramException(gettext('程式成功終止'))
        new_cluster = []
        for attr_id in range(attr_num):
            if attr_id in qi_list:
                if data_dict[column_name[attr_id]]['type'] == 'numerical':
                    new_cluster.append((min(cluster_1[attr_id][0], cluster_2[attr_id][0]), max(cluster_1[attr_id][1], cluster_2[attr_id][1])))
                elif data_dict[column_name[attr_id]]['type'] == 'categorical':
                    new_cluster.append(data_dict[column_name[attr_id]]['category_generalize'][(cluster_1[attr_id], cluster_2[attr_id])])
            else:
                new_cluster.append(cluster_1[attr_id] + cluster_2[attr_id])
        return new_cluster
        
    def force_data_eligible(distribution_dict, distribution, cluster_distribution_dict, cluster_member_num):
        sa_subjects = [ele for ele in cluster_distribution_dict.keys()]
        cluster_distribution = np.array([i for i in cluster_distribution_dict.values()]) / cluster_member_num
        while True:
            if file.skip:
                raise BreakProgramException(gettext('程式成功終止'))
            over_most = sa_subjects[np.argmax(distribution - cluster_distribution)]
            under_most = sa_subjects[np.argmin(distribution - cluster_distribution)]
            cluster_distribution_dict[over_most] += 1
            cluster_distribution_dict[under_most] -= 1
            cluster_distribution = np.array([i for i in cluster_distribution_dict.values()]) / cluster_member_num
            if KLD(distribution, cluster_distribution) <= t:
                break
        new_cluster_sa = [] 
        for key, value in cluster_distribution_dict.items():
            for i in range(value):
                new_cluster_sa.append(key)
        return new_cluster_sa
    
    
    # In[ ]:
    file.num_progress = 10
    file.log = 'Building data information...'
    logging.info('t-Closeness 10%')
    file.save()
    if file.skip:
        raise BreakProgramException(gettext('程式成功終止'))
    
    # First K anonymize
    k_anony_data = [] # [(qi_1_min, qi_1_max), qi_2_category, ..., (qi_n_min, qi_n_max), [SA_data]]
    used_id = []
    current_used_num = 0 
    for id_ in range(0, record_num):
        progress_count = progress_count + 1
        if progress_count%20 == 0 and file.num_progress < 60:
            progress_count = 0
            file.num_progress = file.num_progress + 1
            file.save()
        if id_ in used_id:
            continue
        if record_num - current_used_num < 2 * k:
            candidates = []
            for target_id in range(id_ + 1, record_num):
                if target_id in used_id:
                    continue
                candidates.append((target_id, 0))
        else:
            candidates = [(-1, 0) for i in range(k - 1)] # (id, distance)
            for target_id in range(id_ + 1, record_num): 
                if target_id in used_id:
                    continue
                d = person_distance(original_data[id_], original_data[target_id])
                is_record = False
                for i in range(k - 1):
                    if candidates[i][0] == -1:
                        candidates[i] = (target_id, d)
                        is_record = True
                        break
                if not is_record:
                    for i in range(k - 1):
                        if candidates[i][1] > d:
                            for j in reversed(range(i, k - 1)):
                                candidates[j] = candidates[j - 1]
                            candidates[i] = (target_id, d)
                            break
            for i in reversed(range(len(candidates))):
                if candidates[i][0] == -1:
                    del(candidates[i])
        candidates.append((id_, 0))
        
        # Generate K anonymize data
        k_anony_sub_data = []
        for attr_id in range(attr_num):
            if attr_id in qi_list:
                if data_dict[column_name[attr_id]]['type'] == 'numerical':
                    k_anony_sub_data.append((min([original_data[target_id] for target_id, distance in candidates], key=lambda x: x[attr_id])[attr_id], max([original_data[target_id] for target_id, distance in candidates], key=lambda x: x[attr_id])[attr_id]))
                elif data_dict[column_name[attr_id]]['type'] == 'categorical':
                    category_list = [original_data[target_id][attr_id] for target_id, dist in candidates]
                    generalized_category = category_list[0]
                    for i in range(1, len(category_list)):
                        generalized_category = data_dict[column_name[attr_id]]['category_generalize'][(generalized_category, category_list[i])]
                    k_anony_sub_data.append(generalized_category)
                else:
                    logging.error('t_Closeness unknown attribute type')
                    return
            else:
                k_anony_sub_data.append([original_data[target_id][attr_id] for target_id, dist in candidates])
        k_anony_data.append(k_anony_sub_data)
        for id_, distance in candidates:
            used_id.append(id_)
        current_used_num += len(candidates)
    
    
    # In[ ]:
    file.num_progress = 60
    file.log = 'Building data information...'
    logging.info('t-Closeness 60%')
    file.save()
    if file.skip:
        raise BreakProgramException(gettext('程式成功終止'))
    
    
    # Calculate whole SA's distribution
    distribution_dict = {}
    for index in range(record_num):
        if original_data[index][sa_id] not in distribution_dict:
            distribution_dict[original_data[index][sa_id]] = 1
        else:
            distribution_dict[original_data[index][sa_id]] += 1
    distribution = np.array([i for i in distribution_dict.values()]) / record_num
    
    while True:
        progress_count = progress_count + 1
        if progress_count%20 == 0 and file.num_progress < 99:
            progress_count = 0
            file.num_progress = file.num_progress + 1
            file.save()
        if file.skip:
            raise BreakProgramException(gettext('程式成功終止'))
        # Find ineligible clusters
        above_t_cluster_id = []
        for cluster_id in range(len(k_anony_data)):
            cluster_distribution_dict = {}
            for ele in distribution_dict.keys():
                cluster_distribution_dict[ele] = 0
            for ele in k_anony_data[cluster_id][sa_id]:
                cluster_distribution_dict[ele] += 1
            cluster_distribution = np.array([i for i in cluster_distribution_dict.values()]) / len(k_anony_data[cluster_id][sa_id])
            if KLD(distribution, cluster_distribution) > t:
                above_t_cluster_id.append(cluster_id)
        if len(above_t_cluster_id) == 0:
            break
        elif len(above_t_cluster_id) == 1:
            logging.warning('t_Closeness one cluster above t.')
            cluster_id = above_t_cluster_id[0]
            cluster_distribution_dict = {}
            for ele in distribution_dict.keys():
                cluster_distribution_dict[ele] = 0
            for ele in k_anony_data[cluster_id][sa_id]:
                cluster_distribution_dict[ele] += 1
            k_anony_data[cluster_id][sa_id] = force_data_eligible(distribution_dict, distribution, cluster_distribution_dict, len(k_anony_data[cluster_id][sa_id]))
            break
        
        # Find best target to merging
        target_cluster_id = -1
        min_dist = 0
        cluster_1_data = []
        for attr_id in range(attr_num):
            if attr_id in qi_list:
                if data_dict[column_name[attr_id]]['type'] == 'numerical':
                    cluster_1_data.append((k_anony_data[above_t_cluster_id[0]][attr_id][0] + k_anony_data[above_t_cluster_id[0]][attr_id][1]) / 2)
                elif data_dict[column_name[attr_id]]['type'] == 'categorical':
                    cluster_1_data.append(k_anony_data[above_t_cluster_id[0]][attr_id])
            else:
                cluster_1_data.append(None)
        for cluster_2_index in range(1, len(above_t_cluster_id)):
            cluster_2_id = above_t_cluster_id[cluster_2_index]
            cluster_2_data = []
            for attr_id in range(attr_num):
                if attr_id in qi_list:
                    if data_dict[column_name[attr_id]]['type'] == 'numerical':
                        cluster_2_data.append((k_anony_data[cluster_2_id][attr_id][0] + k_anony_data[cluster_2_id][attr_id][1]) / 2)
                    elif data_dict[column_name[attr_id]]['type'] == 'categorical':
                        cluster_2_data.append(k_anony_data[cluster_2_id][attr_id])
                else:
                    cluster_2_data.append(None)
            dist = person_distance(cluster_1_data, cluster_2_data)
            if target_cluster_id == -1 or dist < min_dist:
                target_cluster_id = cluster_2_id
                min_dist = dist
        
        # Merge two clusters
        k_anony_data.append(merge_k_anony(k_anony_data[above_t_cluster_id[0]], k_anony_data[target_cluster_id]))
        del(k_anony_data[target_cluster_id])
        del(k_anony_data[above_t_cluster_id[0]])
    
    # Generalize numerical attributes
    for attr_id in range(attr_num):
        if attr_id in qi_list:
            if data_dict[column_name[attr_id]]['type'] == 'numerical':
                lower_bounds = []
                upper_bounds = []
                for interval in data_dict[column_name[attr_id]]['interval']:
                    lower_bounds.append(interval[0])
                    upper_bounds.append(interval[1])
                lower_bounds = sorted(lower_bounds, reverse=True)
                upper_bounds = sorted(upper_bounds, reverse=False)
                for cluster_index in range(len(k_anony_data)):
                    for lower_bound in lower_bounds:
                        if k_anony_data[cluster_index][attr_id][0] >= lower_bound:
                            break
                    for upper_bound in upper_bounds:
                        if k_anony_data[cluster_index][attr_id][1] <= upper_bound:
                            break
                    k_anony_data[cluster_index][attr_id] = (lower_bound, upper_bound)
    
    file.num_progress = 99
    file.log = 'Save file...'
    logging.info('t_Closeness save file...')
    file.save()
    if file.skip:
        raise BreakProgramException(gettext('程式成功終止'))
        
    # In[ ]:
    
    df_output = {}
    for column in column_name:
        df_output[column] = []
    for data in k_anony_data:
        record = []
        for attr_id in range(attr_num):
            if attr_id in qi_list:
                if data_dict[column_name[attr_id]]['type'] == 'numerical':
                    record.append(str(data[attr_id][0]) + '-' + str(data[attr_id][1]))
                else:
                    record.append(data[attr_id])
            else:
                record.append(None)
        for sa_index in range(len(data[sa_id])):
            for attr_id in range(attr_num):
                if attr_id == sa_id:
                    df_output[column_name[attr_id]].append(data[sa_id][sa_index])
                else:
                    df_output[column_name[attr_id]].append(record[attr_id])
    df_output = pd.DataFrame(df_output)
    if not os.path.isdir(settings.OUTPUT_ROOT + 't_Closeness/' + username + '/' + directory_name + '/'):
        os.makedirs(settings.OUTPUT_ROOT + 't_Closeness/' + username + '/' + directory_name + '/')
    df_output.to_csv(settings.OUTPUT_ROOT + 't_Closeness/' + username + '/' + directory_name + '/' +  directory_name + '_output.csv', encoding='cp950', index=False, columns=column_name)
    
    file.num_progress = 100
    file.log = 'OVER'
    logging.info('t_Closeness OVER')
    file.save()