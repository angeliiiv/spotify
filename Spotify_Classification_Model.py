# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 19:04:11 2022

@author: angel
"""

# Importing Libraries
import pandas as pd
import os
import seaborn as sns
import numpy as np
import sklearn.model_selection
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 



#import database
df = pd.read_csv('music_database_clean.csv')

"""
This next section is preprocessing our data and splitting it.
"""

# Identifying X and Y columns
x_cols = ['danceability','energy', 'key', 'loudness', 
           'mode', 'speechiness', 'acousticness','instrumentalness', 
           'liveness', 'valence', 'tempo']

y_cols = ['artist']


# Creating train and test splits
X_train, X_test, y_train, y_test = train_test_split(df[x_cols],df[y_cols], train_size = .7,random_state = 0)

"""
Python isn't great at udnerstanding units. We will standardize our data to help transform the data.
"""
# standardizing
scaler = StandardScaler()
X_train_data = scaler.fit_transform(X_train)
X_test_data = scaler.fit_transform(X_test)

"""
Time to create and put the model to the test
"""

# K-Nearest Neighbor
from sklearn.neighbors import KNeighborsClassifier

# Make the model
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

KNN = KNeighborsClassifier(n_neighbors = 4)
KNN.fit(X_train_data, y_train)
print(KNN.score(X_train_data, y_train))

# Making confusion matrix
predictions = KNN.predict(X_train_data)
cm = confusion_matrix(y_train, predictions, labels = KNN.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=KNN.classes_)
disp.plot()
plt.tick_params(axis = 'x', labelrotation=90)
plt.title('CM (Training Data)')
plt.show()

# Confusion Matrix for test data
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
test_predictions = KNN.predict(X_test_data)
cm = confusion_matrix(y_test, test_predictions, labels = KNN.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=KNN.classes_)
disp.plot()
plt.tick_params(axis = 'x', labelrotation=90)
plt.title('CM (Test Data)')
plt.show()