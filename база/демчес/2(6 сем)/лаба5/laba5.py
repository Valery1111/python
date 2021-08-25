# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:57:01 2020

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

xLeft = 0.0
xRight = 1.0
kappa = 1


def InitialCondition(x):
    return (1 + x)/np.sqrt(5)


def SetInitialCondition(function, array, numPoints, h):
    for i in range(numPoints):
        array[i] = function(i * h)


def MakeStepVectorized(uOld, numPoints, h, dt, kappa, uNew):
    courant = kappa * dt / (2 * h * h) 

    # неявная реализация поокоординатных операций с помощью векторизации
    uNew[1:numPoints - 1] = uOld[1:numPoints - 1] \
        + courant * (uOld[2:numPoints] * uOld[2:numPoints] * uOld[1:numPoints - 1] \
                     - 2 * uOld[2:numPoints] * uOld[1:numPoints - 1] * uOld[0:numPoints - 2] \
                     + uOld[0:numPoints - 2] * uOld[0:numPoints - 2] * uOld[1:numPoints - 1] \
                     + 2 * uOld[2:numPoints] * uOld[1:numPoints - 1] * uOld[1:numPoints - 1] \
                     - 4 * uOld[1:numPoints - 1] * uOld[1:numPoints - 1] * uOld[1:numPoints - 1] \
                     + 2 * uOld[0:numPoints - 2] * uOld[1:numPoints - 1] * uOld[1:numPoints - 1]) 
    # boundaries
    uNew[0] = 1/np.sqrt(5 - 4 * (t + dt))
    uNew[-1] = 2/np.sqrt(5 - 4 * (t +dt))
    print(uNew)
    
# main
counter = 0
counterOutput = 0
t, tRun = 0., 1
counterBlocks = 0
numBlocks = 25 #int(1e3)
numPoints = int(numBlocks + 1)
uOld, uNew = np.zeros(numPoints), np.zeros(numPoints)
h = float(xRight - xLeft) / float(numBlocks)
dt = 0.5#h**2 / (kappa * 20.) # h**2 / (kappa * 20.)

                
start = timeit.default_timer()
SetInitialCondition(InitialCondition, uOld, numPoints, h)

while t < tRun:
    
    MakeStepVectorized(uOld, numPoints, h, dt, kappa, uNew)
    
    uOld = uNew
    t += dt; counter += 1

end = timeit.default_timer()
runtime = end - start


xArray = np.linspace(xLeft, xRight, numPoints)
plt.figure(figsize=figsizeConst)
plt.title('Numerical solution')
plt.plot(xArray, uNew, marker='o', color="blue", linewidth=4)
plt.xlabel('x')
plt.ylabel('Temperature')
plt.grid('on')
plt.show()