# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:05:00 2020

@author: ВАЛЕРИЙ
"""

import numpy as np


def analit_u(x, t):
    return 1 + (x + np.exp(t)) * (x + np.exp(t)) - t * t / 2


def phi(x):
    return (x + 1) * (x + 1)


def psi(t):
    return (1 + np.exp(t)) * (1 + np.exp(t)) + t * t / 2


def u_x(t):
    return -2 * (1 + np.exp(t))


def u_xx(t):
    return 2


def u_xxx(t):
    return 0


n = 11
print('L = ', n)
slot_x = [0, 1]
slot_t = [0, 1]
k = 0.5
h = (slot_x[1] - slot_x[0]) / (n - 1)
x_rep = np.linspace(slot_x[0], slot_x[1], 11)
ts = np.linspace(slot_t[0], slot_t[1], n)
print("точки x:")
print(" ".join("%.6E" % x for x in x_rep))
u_analit = [analit_u(x, slot_t[1]) for x in x_rep]
print('Значение следа:')
print(" ".join("%.6E" % i for i in u_analit))
L = n
M = int((L-1)/k)+1
u = [x[:] for x in [[0] * L] * M]
for l in range(L):
    u[0][l] = phi(l * h)
t = h * k
for m in range(1, M):
    psi_m = psi(m * t)
    u[m][L - 1] = psi_m
    u[m][L - 2] = psi_m + u_x(m * t) * h + u_xx(m * t) * h * h / 2
    u[m][L - 3] = psi_m + u_x(m * t) * 2 * h + u_xx(m * t) * h * h * 2
for m in range(M - 1):
    for l in reversed(range(L - 3)):
        u[m + 1][l] = u[m][l] + t / h / 6 * (1 + t / 2 + t * t / 6) * np.exp(m * t) * (
        2 * u[m][l + 3] - 9 * u[m][l + 2] + 18 * u[m][l + 1] - 11 * u[m][l]) + \
                      t * t / h / h / 2 * (1 + t) * np.exp(2 * m * t) * (
                      -u[m][l + 3] + 4 * u[m][l + 2] - 5 * u[m][l + 1] + 2 * u[m][l]) + \
                      t * t * t / h / h / h / 6 * np.exp(3 * m * t) * (
                      u[m][l + 3] - 3 * u[m][l + 2] + 3 * u[m][l + 1] - u[m][l]) + t * (m * t + t / 2)
u_n = u[-1][::int((len(u[0]) - 1) / 10)]
print('Значения численного решения:')
print(" ".join("%.6E" % i for i in u_n))
print('модуль разности следа и отображения численного решения:')
print(" ".join("%.6E" % abs(i - j) for i, j in zip(u_n, u_analit)))
print('Норма:')
print("%.6E" % max([abs(i - j) for i, j in zip(u_n, u_analit)]))
