import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.utils import shuffle
from sklearn.cross_validation import cross_val_score
from math import log

#1. Загрузка данных
data = pd.read_csv("forestfires.csv", sep = ",")
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
months, days = [{elem:i for i,elem in enumerate(arr)} for arr in (months,days)]

#2. Подготовка данных
data['month'] = [months.get(elem, elem) for elem in data['month']]
data['day'] = [days.get(elem, elem) for elem in data['day']]

fit_data = data.iloc[:, 0:12]
answers = data.iloc[:,[12]]

#3. Построение модели L2 регуляризатора
reg_forest = linear_model.Ridge (alpha = .5)
reg_forest.fit(fit_data, answers)
reg_forest.coef_

#Предсказание можно получить, если в качестве коэффициентов подставить reg_forest.coef_
print(reg_forest.coef_)


#4. Обработка. Нарисовать график весов признаков и общей ошибки на кросс-валидации при изменении параметра регуляризации.
data['area'] = [log(x+1) for x in data['area']]
data = shuffle(data)
fit_data = data.iloc[:, 0:12]
answers = data.iloc[:,[12]]

regularization_params = [i/10 for i in range(15)]
coeffs= []
for param in regularization_params:
    model = linear_model.Ridge(param)
    model.fit(fit_data, answers)
    coeffs.append(model.coef_)
for i in range(len(coeffs)):
    coeffs[i] = np.reshape(coeffs[i], (12,))

#4. Графики.

from matplotlib import pyplot as plt
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'FreeSerif'
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 12
plt.rcParams['xtick.labelsize'] = 24
plt.rcParams['ytick.labelsize'] = 24
plt.rcParams['legend.fontsize'] = 16
plt.rcParams['axes.titlesize'] = 36
plt.rcParams['axes.labelsize'] = 24

plt.figure(figsize=(9, 9))
plt.plot(regularization_params, coeffs)
plt.legend(data.columns)
plt.show()


main_features_num = []
for i, coeff in enumerate(coeffs[0]):
    if coeff > 0.04:
        main_features_num.append(i)
plot_y = [[coeffs[param_num][main_feature] for main_feature in main_features_num] for param_num in range(len(coeffs))]
labels = [data.columns[main_feature] for main_feature in main_features_num]

plt.figure(figsize=(9, 9))
plt.plot(regularization_params, plot_y)
plt.legend(labels)
plt.show()

from sklearn.metrics import r2_score, make_scorer

scores = []
for param in regularization_params:
    scores.append(cross_val_score(linear_model.Ridge(alpha=param), fit_data, answers, scoring = make_scorer(r2_score), cv = 5))

#Рассмотрим оценку
print(scores)
