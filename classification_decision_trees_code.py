# -*- coding: utf-8 -*-
"""Галиулина_Классификация_с_помощью_дерева_решений.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lBF6rDMjZ_kjiBTt5NaH_3YAmFg9WOn6
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from datetime import datetime
from tabulate import tabulate
from sklearn import tree
import pandas as pd
import numpy as np
import graphviz

grades_dataset = pd.read_csv("grades.csv")
grades_dataset.info()

# PUPIL_SEX:      Пол ученика
# PUPIL_CLASS:    Класс ученика
# TEACHER_RIGHT:  Процент правильно выполненных заданий
# TEACHER_CHK:    Количество галочек
# TEACHER_QUEST:  Количество вопросиков
# TEACHER_CORR:   Количество исправлений учителя
# PUPIL_CORR:     Количество исправлений ученика
# PUPIL_STRIP:    Количество использований штриха учеником
# GRADE:          Итоговая оценка

grades_dataset.head(10)

grades_dataset.drop('PUPIL_CLASS', axis=1, inplace=True)
grades_dataset['PUPIL_SEX'] = pd.Categorical(grades_dataset['PUPIL_SEX']).codes

# !wget https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv

titanic_dataset = pd.read_csv("titanic.csv")
titanic_dataset.info()

# Survived:                 Выжил ли пассажир
# Pclass:                   Класс пассажира на борту
# Name:                     ФИО пассажира
# Sex:                      Пол пассажира
# Age:                      Возраст пассажира
# Siblings/Spouses Aboard:  Братья, сестры, супруги пассажира на борту 
# Parents/Children Aboard:  Родители, дети пассажира на борту
# Fare:                     Оплаченная стоимость проезда пассажиром

titanic_dataset.head(10)

titanic_dataset.drop('Name', axis=1, inplace=True)
titanic_dataset['Sex'] = pd.Categorical(titanic_dataset['Sex']).codes
titanic_dataset['Survived'] = titanic_dataset['Survived'].astype('string')

accuracy_title = "Аккуратность (accuracy)"
precision_title = "Точность (precision)"
recall_title = "Полнота (recall)"
fscore_title = "F-мера (F-score)"

def get_decision_tree(itemset_attributes, itemset_labels, criteria, part):
  '''
  Получить дерево решений
  : param itemset_attributes: набор атрибутов
  : param itemset_labels: набор меток
  : param criteria: критерий выбора атрибута разбиения (information gain, gini index)
  : param part: доля обучающей выборки от общего размера данных
  :return:
  '''
  class_names = pd.unique(itemset_labels)
  feature_names = list(itemset_attributes.columns)
  X_train, X_test, y_train, y_test = train_test_split(itemset_attributes, itemset_labels, test_size=1-part)
  clf = tree.DecisionTreeClassifier(criterion=criteria)
  clf = clf.fit(X_train, y_train)
  graph = graphviz.Source(tree.export_graphviz(clf, out_file=None, feature_names=feature_names, class_names=class_names, filled=True))
  filename = criteria + '_' + str(datetime.now().time().second) + str(datetime.now().time().microsecond)
  graph.render(filename)
  accuracy = accuracy_score(y_test, clf.predict(X_test))
  precision = precision_score(y_test, clf.predict(X_test), average='weighted', zero_division=1)
  recall = recall_score(y_test, clf.predict(X_test), average='weighted', zero_division=1)
  fscore = f1_score(y_test, clf.predict(X_test), average='weighted', zero_division=1)
  print(tabulate([[accuracy_title, str(accuracy)],
                  [precision_title, str(precision)],
                  [recall_title, str(recall)],
                  [fscore_title, str(fscore)]],
                 headers=['Metric', 'Value']))
  print(tabulate([["Дерево сохранено в " + filename + ".pdf"]]))
  return accuracy, precision, recall, fscore

def get_attributes_and_labels(itemset, label_column):
  '''
  Получить атрибуты и метки класса
  : param itemset: набор данных
  : param label_column: название столбца, содержащего метки класса
  :return:
  '''
  y = itemset.copy()
  X = itemset.copy()
  y = y[label_column]
  X.drop(label_column, axis=1, inplace=True)
  return X, y

grades_attributes, grades_labels = get_attributes_and_labels(grades_dataset, 'GRADE')
titanic_attributes, titanic_labels = get_attributes_and_labels(titanic_dataset, 'Survived')
titanic_labels = titanic_labels.replace('0','Dead')
titanic_labels = titanic_labels.replace('1','Alive')
train_section_size = np.arange(0.6, 1.0, 0.1)
attribute_criteria = ["entropy", "gini"]

def get_classification_quality_indicators(grades_attributes, grades_labels, attribute_criteria):
  accuracies = []
  precisions = []
  recalls = []
  fscores = []
  for section_size in train_section_size:
    accuracy, precision, recall, fscore = get_decision_tree(grades_attributes, grades_labels, attribute_criteria, section_size)
    accuracies.append(accuracy)
    precisions.append(precision)
    recalls.append(recall)
    fscores.append(fscore)
  return accuracies, precisions, recalls, fscores

print('\033[1m' + 'Grades with Information gain' + '\033[0m' + '\n')
grades_accuracy1, grades_precision1, grades_recall1, grades_fscore1 = get_classification_quality_indicators(grades_attributes,
                                                                                                            grades_labels,
                                                                                                            attribute_criteria[0])
print('\n' + '\033[1m' + 'Titanic with Information gain' + '\033[0m' + '\n')
titanic_accuracy1, titanic_precision1, titanic_recall1, titanic_fscore1 = get_classification_quality_indicators(titanic_attributes,
                                                                                                                titanic_labels,
                                                                                                                attribute_criteria[0])
print('\n' + '\033[1m' + 'Grades with Gini index' + '\033[0m' + '\n')
grades_accuracy2, grades_precision2, grades_recall2, grades_fscore2 = get_classification_quality_indicators(grades_attributes,
                                                                                                            grades_labels,
                                                                                                            attribute_criteria[1])
print('\n' + '\033[1m' + 'Titanic with Gini index' + '\033[0m' + '\n')
titanic_accuracy2, titanic_precision2, titanic_recall2, titanic_fscore2 = get_classification_quality_indicators(titanic_attributes,
                                                                                                                titanic_labels,
                                                                                                                attribute_criteria[1])

def show_diagram(grades_y1, titanic_y1, grades_y2, titanic_y2, title):
  x1 = train_section_size - 0.015
  x2 = train_section_size - 0.005
  x3 = train_section_size + 0.005
  x4 = train_section_size + 0.015
  y1 = grades_y1
  y2 = titanic_y1
  y3 = grades_y2
  y4 = titanic_y2

  plt.title(title)
  plt.grid()
  plt.ylim(0.1, 1)
  plt.ylabel('Процент')
  plt.xlabel('Размер обучающей выборки')
  plt.bar(x1, y1, label = 'grades(info)', width = 0.01)
  plt.bar(x2, y2, label = 'titanic(info)', width = 0.01)
  plt.bar(x3, y3, label = 'grades(gini)', width = 0.01)
  plt.bar(x4, y4, label = 'titanic(gini)', width = 0.01)
  plt.legend(loc = 'lower right')
  plt.show()

show_diagram(grades_accuracy1, titanic_accuracy1, grades_accuracy2, titanic_accuracy2, accuracy_title)

show_diagram(grades_precision1, titanic_precision1, grades_precision2, titanic_precision2, precision_title)

show_diagram(grades_recall1, titanic_recall1, grades_recall2, titanic_recall2, recall_title)

show_diagram(grades_fscore1, titanic_fscore1, grades_fscore2, titanic_fscore2, fscore_title)