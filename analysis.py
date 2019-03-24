import json
from os import walk
import numpy as np
from matplotlib import rcParams, cycler
import matplotlib.pyplot as plt
import csv

#import pandas as pd

f = []
for (dirpath, dirnames, filenames) in walk('fhir'):
    f.extend(filenames)
    break

chosen_file = 0

json1_file = open('patients.json')
json1_str = json1_file.read()
p_data = json.loads(json1_str)

print('size of dataset: '+str(len(p_data)))
# for key in p_data[0]:
#     print(key)
#     print(p_data[0][key])

def make_options():
    all_features = []
    all_conditions = []
    for p in p_data:
        for key in p:
            if type(p[key]) is float:
                if key not in all_features:
                    all_features.append(key)
        for c in p['Conditions']:
            if key not in all_conditions:
                all_conditions.append(c[1])
    all_conditions=list(set(all_conditions))
    all_features=list(set(all_features))
    return all_features, all_conditions

def write_all_options(f, c):
    d = {}
    d['Features']=f
    d['Conditions']=c
    with open('options.json', 'w') as outfile:
        json.dump(d, outfile)

def read_options():
    j_file = open('options.json')
    j_str = j_file.read()
    d = json.loads(j_str)
    return d['Features'], d['Conditions']

def make_subset(x_label, y_label, conditions):
    xss, yss = [[] for _ in range(len(conditions)+1)], [[] for _ in range(len(conditions)+1)]
    for p in p_data:
        if x_label in p and y_label in p:
            patients_conditions = [x for (_, x) in p['Conditions']]
            conds = False
            for i in range(len(conditions)):
                if conditions[i] in patients_conditions:
                    xss[i].append(p[x_label])
                    yss[i].append(p[y_label])
                    conds = True
            if not conds:
                xss[len(conditions)].append(p[x_label])
                yss[len(conditions)].append(p[y_label])

    return xss, yss#len xss one longer than conditions

def plot(xss, yss, x_label, y_label, conditions):
    plt.clf()
    fig, ax = plt.subplots()
    cmap = plt.cm.coolwarm # - quite like this one too: viridis
    rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, len(xss))))
    conditions.append('none of these conditions')
    for i in range(len(xss)):
        ax.scatter(xss[i], yss[i], color=cmap(i*(1/len(xss))), marker='.', label=str(conditions[i]))
    ax.legend(loc='upper right', fancybox=True, shadow=True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # plt.plot()
    # plt.show()


def export_dataset(xss, yss, x_label, y_label, cnds, name):
    lengths = [len(xs) for xs in xss]
    X = [[x_label, y_label] + cnds]
    for i in range(len(lengths)):
        for j in range(lengths[i]):
            xs = [yss[i][j], xss[i][j]]
            for k in range(len(cnds)):
                if k == i:
                    xs.append(1)
                else:
                    xs.append(0)
            X.append(xs)
    with open('Datasets/'+name+'.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(X)
    plt.savefig('Datasets/Plot-'+name+'.png', dpi=500)
    csvFile.close()



"""only needs to be done once! (redone if patient.json changes)"""
f, c = make_options()
write_all_options(f, c)


def example():
    x_label = 'Body Mass Index Average'
    y_label = 'Systolic Blood Pressure Average'
    conditions = ['Coronary Heart Disease', 'Stroke', 'Prediabetes', 'Hypertension']
    xss, yss = make_subset(x_label, y_label, conditions)
    plot(xss, yss, x_label, y_label, conditions) 
    plt.show()

if __name__ == '__main__':
    print('want to see an example? (Y/n)')
    s=input()
    if s in ['Y', 'y'] :
        example()
    print('Now try your own')
    f,c=read_options()

    print(f)


    print('\n these are your options for x and y axis\':')
    x_label=''
    while(True):
        print('select x')
        s=input()
        if s in f:
            x_label=s
            break
        else:
            print('not in features list')
    print(s+' selected for x axis')


    y_label=''
    while(True):
        print('select y')
        s=input()
        if s in f and s != x_label:
            y_label=s
            break
        else:
            print('not in features list')
    print(s+' selected for y axis')

    print(c)
    print('\n these are your options for conditions')
    print('select conditions you would like to look at:')
    cnds=[]
    while(True):
        print('select condition')
        s=input()
        if s in c and c not in cnds:
            cnds.append(s)
            print('would you like to add any more? (Y/n)')
            s=input()
            if s not in ['Y', 'y'] :
                break
        else:
            print('not in conditions list')
    print('seleced conditions: '+str(cnds))

    xss, yss = make_subset(x_label, y_label, cnds)
    plot(xss, yss, x_label, y_label, cnds)
    print('Would you like to export this dataset? (Y/n) (as y, X = [x, categorically encoded conditions])')
    s=input()
    if s in ['Y', 'y'] :
        print('Give the filename you would like:')
        s=input()
        export_dataset(xss, yss, x_label, y_label, cnds, s)
    plt.show()
