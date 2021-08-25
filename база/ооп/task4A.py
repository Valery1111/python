# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:51:53 2020

@author: ВАЛЕРИЙ
"""

from task2 import DerivativeNumCommon

import math as m
import numpy as np
import matplotlib.pyplot as plt
import sympy as smp


xSym = smp.Symbol('x')
h = 0.001


class NormaC0:
    def __init__(self, a, b, h):
        self.a = a
        self.b = b
        self.h = h
        self.fun = []
        self.n = int((b - a)/h) + 1
        
    def __call__(self, fx):
        f = smp.lambdify(xSym, fx)
        for i in range(self.n):
            self.fun.append(np.abs(f(self.a + i * self.h)))
        return np.amax(self.fun)
    
    def metric(self, f, g):
        return self.__call__(f - g)
        

class NormaC1(NormaC0):    
    def __init__(self, a, b, h):
        super().__init__(a, b, h)
        self.der_fun = []
        
    def __call__(self, fx):
        super().__call__(fx)
        f = smp.lambdify(xSym, fx)
        self.der = DerivativeNumCommon(f, h)
        self.der.SetA([0, 0, -0.5, 0, 0.5, 0, 0])
        for i in range(self.n + 1):
            self.der_fun.append(np.abs(self.der(self.a + (i - 1) * self.h)))
            #print(self.der_fun[i])
        return np.amax(self.fun) + np.amax(self.der_fun)
'''
p = xSym * xSym
nor1 = NormaC1(0, 2, h)
print(nor1(p))
''' 
class NormaC2(NormaC1):    
    def __init__(self, a, b, h):
        super().__init__(a, b, h)
        self.der2_fun = []
        
    def __call__(self, fx):
        super().__call__(fx)
        for i in range(self.n):
            self.der2_fun.append(np.abs(self.der(self.a + (i + 1) * self.h) - self.der(self.a + (i - 1) * self.h))/(2*self.h))
        return np.amax(self.fun) + np.amax(self.der_fun) +  np.amax(self.der2_fun)


functionsSym = [5/(2 + 3 * xSym*xSym), 2/(5 + smp.cos(xSym)), 2 * smp.exp(-xSym * xSym)/smp.sqrt(m.pi),  (4 * xSym * xSym + 3) **(1/3)]
#functions = [smp.lambdify(xSym, f) for f in functionsSym]

for f in functionsSym:
    nor = NormaC0(0, 2, h)
    nor1 = NormaC1(0, 2, h)
    nor2 = NormaC2(0, 2, h)
    print('Норма функции {0} равна в С0: {1}, в С1: {2}, в С2: {3}'.format(f, nor(f), nor1(f), nor2(f)))

print('Метрика:')
for i in range(3): 
    print('Метрика между {0} и {1} равна в С0: {2}, в С1: {3}, в С2: {4}'.format(functionsSym[0], functionsSym[i+1], nor.metric(functionsSym[0], functionsSym[i+1]), nor1.metric(functionsSym[0], functionsSym[i+1]), nor2.metric(functionsSym[0], functionsSym[i+1])))

for i in range(2): 
    print('Метрика между {0} и {1} равна в С0: {2}, в С1: {3}, в С2: {4}'.format(functionsSym[1], functionsSym[i+2], nor.metric(functionsSym[1], functionsSym[i+2]), nor1.metric(functionsSym[1], functionsSym[i+2]), nor2.metric(functionsSym[1], functionsSym[i+2])))

print('Метрика между {0} и {1} равна в С0: {2}, в С1: {3}, в С2: {4}'.format(functionsSym[2], functionsSym[3], nor.metric(functionsSym[2], functionsSym[3]), nor1.metric(functionsSym[2], functionsSym[3]), nor2.metric(functionsSym[2], functionsSym[3])))
#nor = NormaC2(t, 0, 2, h)
#print(nor.res())
