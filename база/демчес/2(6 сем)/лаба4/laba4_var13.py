# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:25:00 2020

@author: ВАЛЕРИЙ
"""


import numpy as np
import math as m
import matplotlib.pyplot as plt
import time
import timeit
import numba as nb

figsizeConst = (11.6, 7.)
plt.rc('font', size=20)

xLeft = 0.
xRight = 1.

def analit(x):
    return (1 + np.exp(x)) **2 + np.exp(x) - x * np.exp(x)


def InitialCondition(x):
    return np.exp(2 * x) - (x - 1) * np.exp(x)


def SetInitialCondition(function, array, numPoints, h):
    for i in range(numPoints):
        array[i] = function(i * h)

    
def MakeStepVectorized(uOld, numPoints, h, dt, uNew, x, t):
    courant = dt / (2 * h) 
    # неявная реализация поокоординатных операций с помощью векторизации
    uNew[0:numPoints-2] = uOld[0:numPoints-2] \
                          - courant * np.exp(-x[0:numPoints-2]) * (1-dt * np.exp(-x[0:numPoints-2])/2) \
                          * (uOld[2:numPoints] - 4*uOld[1:numPoints-1] + 3*uOld[:numPoints-2]) \
                          + 2 * courant * courant * np.exp(-2 * x[0:numPoints-2]) \
                          * (uOld[2:numPoints] - 2*uOld[1:numPoints-1] + uOld[:numPoints-2]) \
                          + dt * (x[0:numPoints-2] + dt * np.exp(-x[0:numPoints-2])/2)
                                                        

    # boundaries
    uNew[-1] = (np.exp(1) + t) ** 2
    uNew[-2] = (uNew[-3] + uNew[-1]) / 2

# main
my_file = open("labo4.txt", "w")
xixi = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
#uAnalit = [analit(i) for i in xixi]
uAnalit = np.zeros(11)
for i in range(11):
    uAnalit[i] = analit(xixi[i])


eN = [11, 21, 41, 81, 161, 321, 641, 1281, 2561, 5121]
for n in eN:
    t, tRun = 0., 1.
    numBlocks = n-1 #int(1e3)
    numPoints = int(numBlocks + 1)
    uOld, uNew = np.zeros(numPoints), np.zeros(numPoints)#, np.zeros(numPoints)
    h = float(xRight - xLeft) / float(numBlocks)
    dt = 0.0005 # h**2 / (kappa * 20.)

                
    start = timeit.default_timer()
    SetInitialCondition(InitialCondition, uOld, numPoints, h)
    #SetInitialCondition(analit, uAnalit, numPoints, h)

    xArray = np.linspace(xLeft, xRight, numPoints)

    while t < tRun:
        t += dt
        MakeStepVectorized(uOld, numPoints, h, dt, uNew, xArray, t)
    
        uOld = uNew
    
    
    p = int(numBlocks/10)
    print('Analitical:', uAnalit)
    print(' Numerical:', uNew[::p])
    print('differ:', abs(uNew[::p] - uAnalit))
    end = timeit.default_timer()
    runtime = end - start
    print ('\n Calculations took ... %.2e s' % runtime)
    
    #ochen krivoruko
    an = uAnalit
    re = uNew[::p]
    di = abs(uNew[::p] - uAnalit)
    str1, str2, str3 = [], [], []
    for i in range(11):
        str1.append(float('{:.6f}'.format(an[i])))
        str2.append(float('{:.6f}'.format(re[i])))
        str3.append(float('{:.6f}'.format(di[i])))

    my_file.write('\nN: ')
    my_file.write(str(n))
    xi = '       '.join(str(i) for i in xixi)
    my_file.write('\n      Step:        ')
    my_file.write(xi)
    my_file.write('\nAnalitical:      ')
    suAnalit = '  '.join(str(i) for i in str1)
    sNum = '  '.join(str(i) for i in str2)
    diff = '  '.join(str(i) for i in str3)
    my_file.write(suAnalit)
    my_file.write('\n Numerical: ')
    my_file.write(sNum)
    my_file.write('\nDifference: ')
    my_file.write(diff)
    my_file.write('\n ')
    my_file.write('\n ')
my_file.close()
'''
plt.figure(figsize=figsizeConst)
plt.plot(xArray, uNew, 'b-', linewidth=4, label='Numerical')
plt.plot(xArray, uAnalit, 'r-', linewidth=4, label='Analitical')
plt.legend()
plt.xlabel('x')
plt.ylabel('Temperature')
plt.grid('on')
plt.show()
'''
