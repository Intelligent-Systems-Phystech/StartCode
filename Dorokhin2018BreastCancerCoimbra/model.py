print(__doc__)
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler

#age,BMI,Glucose,Insulin,HOMA,Leptin,Adiponectin,Resistin,MCP.1,Classification

plot_args = [{'c': 'red', 'linestyle': '-'},
        {'c': 'green', 'linestyle': '-'},
        {'c': 'blue', 'linestyle': '-'},
        {'c': 'orange', 'linestyle': '--'},
        {'c': 'magenta', 'linestyle': '--'},
        {'c': 'black', 'linestyle': '--'}]

labels = ["116 samples", "96 samples", "76 samples", "5 samples messed", "15 samples messed", "40 samples messed"]
attr_nu = 10
with open ('dataR2.csv', newline = '') as csvfile:
    data = list(csv.reader(csvfile, delimiter = ','))
    sample_nu = int (sum (1 for row in data))
    train = np.zeros (shape = (sample_nu, attr_nu))
    for i, row in enumerate (data):
        for j, attr in enumerate (row):
            train [i, j] = attr    
max_i = 40
fig, ax = plt.subplots (1, 1, figsize = (18, 10))
max_iter = 3000
for j, i in enumerate (np.linspace (0, max_i, 3)):
    X = train[int (i / 2 + i % 2):sample_nu - int(i / 2), 0:9]
    y = train[int (i / 2 + i % 2):sample_nu - int(i / 2), 9]

    X = MinMaxScaler().fit_transform(X)
    mlps = []
    mlp = MLPClassifier(verbose=0, random_state=0, max_iter=max_iter)
    mlp.fit(X, y)
    mlps.append(mlp)
    print ("Training set score: %f" % mlp.score (X, y))
    print ("Training set loss: %f" % mlp.loss_)
    ax.plot(mlp.loss_curve_, label = labels[j], **plot_args[j])
for l_n, swap_nu in enumerate ({5, 15, 40}):
    X = train[0:sample_nu, 0:9]
    y = train[0:sample_nu, 9]
    for i in range (1, swap_nu):
        ind1 = int (np.random.uniform(0, sample_nu - 1))
        ind2 = int (np.random.uniform(0, sample_nu - 1)) 
        j1 = int (np.random.uniform(1, 8)) 
        j2 = int (np.random.uniform(1, 8)) 
        tmp = X[ind1, j1]
        X[ind2, j2] = tmp
        X[ind1, j1] = X[ind2, j2]
    X = MinMaxScaler().fit_transform(X)
    mlp = MLPClassifier(verbose=0, random_state=0, max_iter=max_iter)
    mlp.fit(X, y)
    print ("Training set score: %f" % mlp.score (X, y))
    print ("Training set loss: %f" % mlp.loss_)
    ax.plot(mlp.loss_curve_, label = labels[j + l_n], **plot_args[j + l_n + 1])
fig.legend (ax.get_lines (), labels, ncol = 2, loc = 9)
plt.savefig('learning_curve.png')
plt.show()
