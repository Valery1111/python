# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:47:37 2020

@author: ВАЛЕРИЙ
"""



  
import numpy as np
import matplotlib.pyplot as plt

x_l = 0
x_r = 1
x_0 = 1/2

q_1 = 1
q_2 = 2

for n in range(10, 11):
    L = int(1e6 / 2**n)
    even = L % 2
    h = (x_r - x_l) / (L - 1)


    def f(x):

        determinant_1 = 1
        determinant_i = 1

        b = np.ones(L - 1)
        c = np.ones(L - 1)
        b[0] = c[L - 2] = 0

        a = np.ones(L)
        a[1:int(L * x_0 / (x_r - x_l))] = x * h**2 * q_1 - 2
        a[int(L * x_0 / (x_r - x_l)):-1] = x * h**2 * q_2 - 2

        for i in range(1, L):
            old_determinant_i = determinant_i
            #print(old_determinant_i)
            determinant_i = a[i] * old_determinant_i - c[i - 1] * b[i - 1] * determinant_1
            #print(determinant_i)
            determinant_1 = old_determinant_i

        return -determinant_i


    # Модельная задача

    #q_1 = 1
    #q_2 = 1

    #lambdas = np.arange(4, 500, 0.1)
    #ls = [np.pi**2 * n**2 for n in range(1,8)]

    #func = [f(x) for x in lambdas]
    #plt.plot(lambdas, func, label='determinant(lamda)')
    #plt.plot(ls, np.zeros(7), 'o', label='pi^2*n^2, n = 1,...')
    #plt.legend()
    #plt.show()
    #print('shag', n)
    # Локализация корней

    #q_1 = 1
    #q_2 = 1

    lambdas = np.arange(4, 230, 1)

    func = [f(x) for x in lambdas]
    plt.plot(lambdas, func, color = 'green')
    plt.legend()
    plt.plot([0, 230], [0, 0], color = 'red')
    plt.show()
    
    print('shag', n)

    # Поиск корнейээ

    epsilon = 1e-6

    lambda_0, lambda_1 = 100, 120
    lambda_i = 0
'''
    while (abs(lambda_1 - lambda_0) > epsilon):
        lambda_i = (lambda_0 + lambda_1) / 2
        determinant_i = f(lambda_i)

        if (even == 1):
            if (np.sign(determinant_i) > 0):
                lambda_0 = lambda_i

            if (np.sign(determinant_i) < 0):
                lambda_1 = lambda_i
        else:
            if (np.sign(determinant_i) < 0):
                lambda_0 = lambda_i

            if (np.sign(determinant_i) > 0):
                lambda_1 = lambda_i

    print("L = " + str(L) + "; Root: " + str(lambda_i) + "; Determinant: " + str(f(lambda_i)))
'''