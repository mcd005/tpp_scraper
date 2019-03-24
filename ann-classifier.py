import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import keras
from keras.models import Sequential
from keras.layers import Dense



files = []
for (dirpath, dirnames, filenames) in os.walk(os.getcwd()+'/Datasets/'):
    files.extend(filenames)
    break
files = [f for f in files if f[-4:] == '.csv']
print(files)
print('Which file would you like to use? [0, 1,...]')
s=input()
if s in [str(i) for i in range(len(files))] :
	chosen_file = files[int(s)]

	dataset = pd.read_csv(os.getcwd()+'/Datasets/'+chosen_file)

	(n, p) = dataset.shape
	print(list(dataset))
	print('Which column would you like ot use as your response?')
	s=input()
	if s in [str(i) for i in range(p)]:
		y_col = int(s)
		response = list(dataset)[y_col]

		li = list(range(y_col))+list(range(y_col+1, p))
		X = dataset.iloc[:, li].values
		y = dataset.iloc[:, y_col].values


		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


		sc = StandardScaler()
		X_train = sc.fit_transform(X_train)
		X_test = sc.transform(X_test)


		classifier = Sequential()

		classifier.add(Dense(output_dim = 4, init = 'uniform', activation = 'relu', input_dim = p-1))
		classifier.add(Dense(output_dim = 4, init = 'uniform', activation = 'relu'))
		classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

		classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

		classifier.fit(X_train, y_train, batch_size = 20, nb_epoch = 100)

		y_pred = classifier.predict(X_test)
		y_pred = (y_pred > 0.5)

		cm = confusion_matrix(y_test, y_pred)
		print('confusion_matrix:')
		print(cm)
		TN, FP = cm[0][0], cm[0][1]
		FN, TP = cm[1][0], cm[1][1]
		total = TN+FP+FN+TP
		print('Predicted number of people with '+response+' is '+str(FP+TP))
		print('Predicted number of people not with '+response+' is '+str(TN+FN))
		print('Actual number of people with '+response+' is '+str(FN+TP))
		print('Actual number of people not with '+response+' is '+str(TN+FP))
		print('Accuracy = '+str((TP+TN)/total))
		print('True Positive Rate = '+str(TP/(FN+TP)))
		print('False Positive Rate = '+str(FP/(TN+FP)))
		print('True Negative Rate = '+str(TN/(TN+FP)))
		print('Precision = '+str(TP/(FP+TP)))
		print('Prevalence = '+str((FN+TP)/total))
	else:
		print('Invalid input.')
else:
	print('Invalid input.')