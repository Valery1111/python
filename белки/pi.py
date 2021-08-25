# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 22:16:40 2020

@author: ВАЛЕРИЙ
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
import sympy as smp
import random


plt.figure(figsize=(10, 10))
a, b = 40, 40 #видимая зона графика
r = 5     #длина иглы
L = 4     #расстояние между полосами
num_igl = 500    #количество иголок
n = int(m.modf(b/L)[1])
l = []
l.append(-3 * L)
for i in range(n + 6):
    l.append(l[i] + L)
    if i > 2 and i < n + 3:
        plt.plot([0, a],[l[i+1], l[i+1]], color="grey")
k = 0
for j in range(num_igl):
    ii = 0
    y0 = random.uniform(0, b)
    x0 = random.uniform(0, a)
    fi = random.uniform(0, 628)
    y = y0 + r * np.sin(fi)
    x = x0 + r * np.cos(fi)
    plt.plot([x0, x], [y0, y], color="red")
    for i in range(n + 6):
        if y0 == l[i]:
            k += 1
            ii = i
        elif y0 > l[i] and y0 < l[i + 1]:
            ii = i
    left, right = ii, ii + 1

    while y <= l[left]:
        k += 1
        left -= 1
    while y >= l[right]:
        k += 1
        right += 1
print('Количество пересеченных игл:', k)
p = k/num_igl
pi = (2 * r) / (L * p)
print('Число пи: ', '%.3f' % pi)
plt.xlim (0, a)
plt.ylim (0, b)
plt.show()       

