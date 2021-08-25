# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:16:54 2020

@author: ВАЛЕРИЙ
"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
import sympy as smp
import random

x0 = 1.5
xSym = smp.Symbol('x')
# наша старая функция
fSym = xSym**2 * smp.sin(2 * smp.pi * xSym)


class AntiderivativeAbstract():
    
    def __init__(self, f, xLeft, numBlocks):
        self.f = f
        self.xLeft = xLeft # xLeft = a
        self.numBlocks = numBlocks
        self._a = []
        self._gridPoints = []
        
    def SetA(self, a):
        self._a = a
        
    def SetP(self, gridPoints):
        self._gridPoints = gridPoints
        
    def __call__(self, x):
        x = float(x)
        a, f, gridPoints = self._a, self.f, self._gridPoints
        h = (x - self.xLeft)/self.numBlocks
        if len(gridPoints) == 0:
            gridPoints = np.linspace(self.xLeft, x, self.numBlocks + 1)
        ef = []
        for i in range(len(gridPoints)):
            efi = f(gridPoints[i])
            ef.append(efi) 
        return h * np.dot(a, ef)
   
    
class AntiderivativeSecond(AntiderivativeAbstract):
    def __init__(self, f, xLeft, numBlocks):
        super().__init__(f, xLeft, numBlocks)
        self._a.append(0)
        for i in range(self.numBlocks):
            self._a.append(1)
 
           
class AntiderivativeThird(AntiderivativeAbstract):
    def __init__(self, f, xLeft, numBlocks):
        super().__init__(f, xLeft, numBlocks)
        self._a.append(1)
        for i in range(self.numBlocks - 1):
            self._a.append(1)
        self._a.append(0)
        

class AntiderivativeFourth(AntiderivativeAbstract):
    def __init__(self, f, xLeft, numBlocks):
        super().__init__(f, xLeft, numBlocks)
        self._a.append(1)
        for i in range(self.numBlocks - 1):
            self._a.append(1)
        self._a.append(0)
        
    def __call__(self, x):
        x = float(x)
        a, f, gridPoints = self._a, self.f, self._gridPoints
        h = (x - self.xLeft)/self.numBlocks
        if len(gridPoints) == 0:
            gridPoints = np.linspace(self.xLeft+h/2, x+h/2, self.numBlocks +1)
        ef = []
        for i in range(len(gridPoints)):
            efi = f(gridPoints[i])
            ef.append(efi) 
        return h * np.dot(a, ef)
    

class AntiderivativeFifth(AntiderivativeAbstract):
    def __init__(self, f, xLeft, numBlocks):
        super().__init__(f, xLeft, numBlocks)
        self._a.append(1/2)
        for i in range(self.numBlocks - 1):
            self._a.append(1)
        self._a.append(1/2)
        
        
class AntiderivativeSixth(AntiderivativeAbstract):
    def __init__(self, f, xLeft, numBlocks):
        super().__init__(f, xLeft, numBlocks)
        self._a.append(1/3)
        for i in range(int(self.numBlocks/2) - 1):
            self._a.append(4/3)
            self._a.append(2/3)
        self._a.append(4/3)
        self._a.append(1/3)


class MonteCarloSimple(AntiderivativeAbstract):
    def __call__(self, x):
        x = float(x)
        f = self.f
        Sum = 0
        for i in range(self.numBlocks):
            Sum += f(random.uniform(self.xLeft, x))
        return (x - self.xLeft) * Sum / self.numBlocks

       
class MonteCarloGeom(AntiderivativeAbstract):
    def __call__(self, x):
        x = float(x)
        f = self.f
        b = 1.5
        k = 0
        for i in range(self.numBlocks):
            if f(random.uniform(self.xLeft, x)) >= random.uniform(0, b):
                k += 1
        return (x - self.xLeft) * b * k / self.numBlocks

functionsSym = [smp.sin(xSym*xSym)]#, smp.cos(smp.sin(xSym)), smp.exp(smp.sin(smp.cos(xSym))), smp.log(xSym + 3), smp.sqrt(xSym + 3)]
# генерируем "обычные" функции из символьных: этим занимается функция lambdify
functions = [smp.lambdify(xSym, f) for f in functionsSym]# выводим значения всех функций на экран
valuesAnalyticalSym = [smp.integrate(f, (xSym, 0., x0)) for f in functionsSym]
figureSizeConst = (13, 6.7)

steps = [2**(n+1) for n in range(0, 14)]


for f, valueAnalytical,  in zip(functions, valuesAnalyticalSym):
        plt.figure(figsize=figureSizeConst)
        plt.title('Анализ сходимости sin(x)^2')
        errors = []
        for h in steps:
            
            ant = AntiderivativeSecond(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выше
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
        errors = []
        
        for h in steps:
            ant = AntiderivativeThird(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выше
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
        
        errors = []
        for h in steps:
            ant = AntiderivativeFourth(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выше
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)

        errors = []
        for h in steps:
            ant = AntiderivativeFifth(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выше
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)

        errors = []
        for h in steps:
            ant = AntiderivativeSixth(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выше
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
        
        errors = []
        for h in steps:
            ant = MonteCarloSimple(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выш
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
        
        errors = []
        for h in steps:
            ant = MonteCarloGeom(f, xLeft=0., numBlocks=h)
            error = m.fabs(ant(x0) - valueAnalytical)
            errors.append(error)
            # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выш
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
        
        
        plt.legend(('AntiderivativeSecond', 'AntiderivativeThird', 'AntiderivativeFourth', 'AntiderivativeFifth', 'AntiderivativeSixth',  'MonteCarloSimple', 'MonteCarloGeom'))
        plt.xlabel('Шаг сетки')
        plt.ylabel('Погрешность')
        plt.show()
'''
n = 10000
print('Analitical: ', '%.5f' % float(valuesAnalyticalSym[0]))
a = AntiderivativeSecond(functions[0], xLeft=0., numBlocks=n)
print('AntiderivativeSecond: ', '%.5f' % a(x0))
b = AntiderivativeThird(functions[0], xLeft=0., numBlocks=n)
print('AntiderivativeThird: ', '%.5f' % b(x0))
c = AntiderivativeFourth(functions[0], xLeft=0., numBlocks=n)
print('AntiderivativeFourth: ', '%.5f' % b(x0))
d = AntiderivativeFifth(functions[0], xLeft=0., numBlocks=n)
print('AntiderivativeFifth: ', '%.5f' % d(x0))
e = AntiderivativeSixth(functions[0], xLeft=0., numBlocks=n)
print('AntiderivativeSixth: ', '%.5f' % e(x0))
an = MonteCarloSimple(functions[0], xLeft=0., numBlocks=n)
print('MonteCarSimple: ', '%.5f' % an(x0))
ant = MonteCarloGeom(functions[0], xLeft=0., numBlocks=n)
print('MonteCarloGeom: ', '%.5f' % ant(x0))
'''
