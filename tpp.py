import json
from os import walk
import numpy as np

f = []
for (dirpath, dirnames, filenames) in walk('fhir'):
    f.extend(filenames)
    break

chosen_file = 0

json1_file = open('fhir/'+f[chosen_file])
json1_str = json1_file.read()
json1_data = json.loads(json1_str)

# data = json1_data['entry']

#a = patient_data(f[0])
def patient_data(name):
    conditions = []
    json1_file = open('fhir/'+name)
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    
    observations = []
    
    data = json1_data['entry']
    
    g_dets = {}
    dets = ['birthDate', 'id', 'gender']
    general_dets = data[1]['resource']
    if 'address' in general_dets:
        if 'state' in general_dets['address'][0]:
            g_dets['State'] = general_dets['address'][0]['state']
        else:
            g_dets['State'] = ''
        if 'City' in general_dets['address'][0]:
            g_dets['City'] = general_dets['address'][0]['city']
        else:
            g_dets['City'] = ''
    for key in dets:
        if key in general_dets:
            g_dets[key] = general_dets[key]
        else:
            g_dets[key] = ''
    
    for i in range(len(data)):
    #    print(data[i]['resource']['resourceType'])
        if data[i]['resource']['resourceType'] == 'Observation':
            resource = data[i]['resource']
            
            date = resource['effectiveDateTime']
            code = resource['code']['coding'][0]['code']
            display = resource['code']['coding'][0]['display']
            if display == 'Blood Pressure':
                value = ( resource['component'][0]['valueQuantity']['value'], resource['component'][1]['valueQuantity']['value'])
            elif 'valueQuantity' in resource:
    #        print(resource)
    #        value = ''
    #        if 'valueQuantity' in resource:
                value = resource['valueQuantity']['value']
            else:
                value = 0
            observations.append( [date, code, display, value] )
        elif data[i]['resource']['resourceType'] == 'Condition':
            d = data[i]['resource']['assertedDate']
            cond = data[i]['resource']['code']['coding'][0]['display']
            conditions.append( [d, cond] )
            
    dict_ = {}
    for obs in observations:
        categ = obs[2]
        if categ in dict_:
            dict_[categ] += [(obs[0], obs[3])]
        else:
            dict_[categ] = [(obs[0], obs[3])]
    if 'Blood Pressure' in dict_:
        dict_['Systolic Blood Pressure'] = [ (date, sys) for (date, (sys, dia)) in dict_['Blood Pressure'] ]
        dict_['Diastolic Blood Pressure'] = [ (date, dia) for (date, (sys, dia)) in dict_['Blood Pressure'] ]
        del dict_['Blood Pressure']
    return g_dets, dict_, conditions

def convert(date):#2009-07-27T06:47:32-04:00
    yr = int(date[0:4])
    m  = int(date[5:7])
    d  = int(date[8:10])
    return yr + m/12 + (d/30)/12
    
def simplify_obs(obs):
    observations = {}
    for o in obs:
        values = obs[o]
        dates, values = zip(*values)
        dates = [ convert(date) for date in dates ]
        '''use grad of line of best fit, average, range    (maybe improve with pca variences) '''
        average = sum(values)/len(values)
        range_ = max(values) - min(values)
        x = np.unique(dates)
        y = np.poly1d(np.polyfit(dates, values, 1))(np.unique(dates))
        grad = 0
        if x[-1]-x[0] != 0:
            grad = (y[-1]-y[0])/(x[-1]-x[0])
        observations[o] = [grad, average, range_]
    return observations


patients = []

for i in range(len(f)):
    print(f[i])
    new_dict, obs, conditions = patient_data(f[i])
#    new_dict, obs, conditions = patient_data(name)
    obs_simplified = simplify_obs(obs)
#    new_dict = {}
    stat = [' Gradient', ' Average', ' Range']
    for key in obs_simplified:
        if len(obs_simplified[key]) == 1:
            new_dict[key] = obs_simplified[key]
        else:
            for i in range(len(obs_simplified[key])):
                new_dict[key+stat[i]] = obs_simplified[key][i]
    new_dict['Conditions'] = conditions
    patients.append(new_dict)
#    for i in range(len(conditions)):
#        new_dict['Condition '+str(i)] = conditions[i][1]
#        new_dict['Condition Date '+str(i)] = conditions[i][0]
#    patients.append(new_dict)
        
with open('patients.json', 'w') as outfile:
    json.dump(patients, outfile)



def age(d1, d2):
    yr1, yr2 = int(d1[0:4]), int(d2[0:4])
    m1, m2 = int(d1[5:7]), int(d2[5:7])
    age = yr2 - yr1
    m = m2 - m1
    return abs(age + m/12)
