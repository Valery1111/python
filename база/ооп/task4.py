# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:40:38 2020

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
    def __init__(self, f, a, b, h):
        self.f = f
        self.a = a
        self.b = b
        self.h = h
        self.fun = []
        self.n = int((b - a)/h) + 1
        for i in range(self.n):
            self.fun.append(np.abs(f(a + i * h)))
        self.max_fun = np.amax(self.fun)
        
    def res(self):
        return self.max_fun


class NormaC1(NormaC0):    
    def __init__(self, f, a, b, h):
        super().__init__(f, a, b, h)
        self.der_fun = []
        self.der = DerivativeNumCommon(f, h)
        self.der.SetA([0, 0, -0.5, 0, 0.5, 0, 0])
        for i in range(self.n + 2):
            self.der_fun.append(np.abs(self.der(a + (i - 1) * h)))
        self.max_der_fun = np.amax(self.der_fun)
        
    def res(self):
        return self.max_fun + self.max_der_fun

    
class NormaC2(NormaC1):    
    def __init__(self, f, a, b, h):
        super().__init__(f, a, b, h)
        self.der2_fun = []
        for i in range(self.n):
            self.der2_fun.append(np.abs(self.der(a + (i + 1) * h) - self.der(a + (i - 1) * h))/(2*h))
        self.max_der2_fun = np.amax(self.der2_fun)
        
    def res(self):
        return self.max_fun + self.max_der_fun + self.max_der2_fun

if __name__ == "__main__":
    functionsSym = [5/(2 + 3 * xSym*xSym), 2/(5 + smp.cos(xSym)), 2 * smp.exp(-xSym * xSym)/smp.sqrt(m.pi),  (4 * xSym * xSym + 3) **(1/3)]
    functions = [smp.lambdify(xSym, f) for f in functionsSym]

    for f, x in zip(functions, functionsSym):
        nor = NormaC0(f, 0, 2, h)
        nor1 = NormaC1(f, 0, 2, h)
        nor2 = NormaC2(f, 0, 2, h)
        print('Норма функции {0} равна в С0: {1}, в С1: {2}, в С2: {3}'.format(x, nor.res(), nor1.res(), nor2.res()))

    print('Метрика:')
    for i in range(3): 
        f = smp.lambdify(xSym, functionsSym[0] - functionsSym[i+1])
        nor = NormaC0(f, 0, 2, h)
        nor1 = NormaC1(f, 0, 2, h)
        nor2 = NormaC2(f, 0, 2, h)
        print('Метрика между {0} и {1} равна в С0: {2}, в С1: {3}, в С2: {4}'.format(functionsSym[0], functionsSym[i+1], nor.res(), nor1.res(), nor2.res()))
    for i in range(2): 
        f = smp.lambdify(xSym, functionsSym[1] - functionsSym[i+2])
        nor = NormaC0(f, 0, 2, h)
        nor1 = NormaC1(f, 0, 2, h)
        nor2 = NormaC2(f, 0, 2, h)
        print('Метрика между {0} и {1} равна в С0: {2}, в С1: {3}, в С2: {4}'.format(functionsSym[1], functionsSym[i+2], nor.res(), nor1.res(), nor2.res()))
    f = smp.lambdify(xSym, functionsSym[2] - functionsSym[3])
    nor = NormaC0(f, 0, 2, h)
    nor1 = NormaC1(f, 0, 2, h)
    nor2 = NormaC2(f, 0, 2, h)
    print('Метрика между {0} и {1} равна в С0: {2}, в С1: {3}, в С2: {4}'.format(functionsSym[2], functionsSym[3], nor.res(), nor1.res(), nor2.res()))

