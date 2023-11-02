from snsynth import Synthesizer
import pandas as pd
import numpy as np
import swifter
import copy

eps = 10.0
nhanes = pd.read_csv("NHANES.csv")
gen_num = nhanes.shape[0]
print('Total number:', gen_num)

attr_info_1 = {'RIDAGEYR':[32, 44, 56, 68], 'BMXBMI':[28, 42, 56, 70], 'LBXGH':[7, 9, 12, 14], 'METS':[12000, 230000, 35000, 46000]} ## interval
attr_info_2 = {'RIDAGEYR':[20, 81], 'BMXBMI':[14, 85], 'LBXGH':[4, 17], 'METS':[0, 58321]} ## min-max value
## ==> RIDAGEYR(5 intervals): [20, 31], [32, 43], [44, 55], [56, 67], [68, 80]


def value_dispatch_1(v, conditions):
    s = ['A', 'B', 'C', 'D', 'E']
    if v < conditions[0]:
        return s[0]
    elif v < conditions[1]:
        return s[1]
    elif v < conditions[2]:
        return s[2]
    elif v < conditions[3]:
        return s[3]
    else:
        return s[4]

def value_dispatch_2(v, conditions):
    if v == 'A':
        return np.random.randint(conditions[0][0], conditions[0][1])
    elif v == 'B':
        return np.random.randint(conditions[1][0], conditions[1][1])
    elif v == 'C':
        return np.random.randint(conditions[2][0], conditions[2][1])
    elif v == 'D':
        return np.random.randint(conditions[3][0], conditions[3][1])
    else:
    	return np.random.randint(conditions[4][0], conditions[4][1])

num_attr = list(attr_info_1.keys())
for attr in num_attr:
	nhanes[attr] = nhanes[attr].swifter.apply(value_dispatch_1, args=(attr_info_1[attr],))

synth = Synthesizer.create('pacsynth', epsilon=eps, verbose=True)
synth.fit(nhanes, preprocessor_eps=0.0, nullable=False)

output = pd.DataFrame()
continue_syn = True
syn_num = copy.deepcopy(gen_num)
while continue_syn:
	output = synth.sample(syn_num)
	output.dropna(inplace=True)
	count = output.shape[0]
	if count == gen_num:
		continue_syn = False
		print('syn_num:', syn_num, 'valid_num:', count, '<--- Completed!')
	else:
		print('syn_num:', syn_num, 'valid_num:', count)
		syn_num += (gen_num - count)

attr_reverse = {}
for attr in num_attr:
	tmp = []
	for idx in range(5):
		if idx == 0:
			tmp.append([attr_info_2[attr][0], attr_info_1[attr][0]])
		elif idx == 4:
			tmp.append([attr_info_1[attr][3], attr_info_2[attr][1]])
		else:
			tmp.append([attr_info_1[attr][idx-1], attr_info_1[attr][idx]])
	attr_reverse[attr] = tmp
	del tmp

for attr in num_attr:
	output[attr] = output[attr].swifter.apply(value_dispatch_2, args=(attr_reverse[attr],))


output.to_csv('result.csv', index=0)

