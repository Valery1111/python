

import math as m
import numpy as np
import matplotlib.pyplot as plt
import sympy as smp
xSym = smp.Symbol('x')


x0 = 5.
h0 = 1e-4

class DerivativeNumCommon:
    
    def __init__(self, f, h):
        self.f = f
        self.h = h
        
        
    def SetA(self, a):
        self._a = a
        

    def __call__(self, x):
        f = self.f
        h = self.h
        a = self._a
        return (a[0] * f(x - 3 * h) + a[1] * f(x - 2 * h) + a[2] * f(x - h) + a[3] * f(x) + a[4] * f(x + h) + a[5] * f(x + 2 * h) + a[6] * f(x + 3 * h))/h


ay = ([0, 0, 0, -1, 1, 0, 0], [0, 0, -1, 1, 0, 0, 0], [0, 0, -0.5, 0, 0.5, 0, 0], [0, 1/12, -2/3, 0, 2/3, -1/12, 0], [-1/60, 3/20, -3/4, 0, 3/4, -3/20, 1/60])



functionsSym = [smp.sin(xSym*xSym), smp.cos(smp.sin(xSym)), smp.exp(smp.sin(smp.cos(xSym))), smp.log(xSym + 3), smp.sqrt(xSym + 3)]
functions = [smp.lambdify(xSym, f) for f in functionsSym]


complex = []
n = [0, 1, 2, 3, 4]
der = [0, 0, 0, 0, 0]

if __name__ == "__main__":
    figureSizeConst = (13, 6.7) # в дюймах

    derivativesAnalyticalSym = [smp.diff(f, xSym) for f in functionsSym]

# символьное дифференцирование; используем генераторы списков
    derivativesAnalytical = [smp.lambdify(xSym, f) \
                       for f in derivativesAnalyticalSym]
  
    steps = [2**(-n) for n in range(1, 21)]



    for f, derivativeAnalytical in zip(functions, derivativesAnalytical):
            plt.figure(figsize=figureSizeConst)
            plt.title('Анализ сходимости')
            #i = 3    
            for i in n:
                errors = []
                for h in steps:
                    der[i] = DerivativeNumCommon(f, h)
                    der[i].SetA(ay[i])
                    error = m.fabs(der[i](x0) - derivativeAnalytical(x0))
                    errors.append(error)
                # на каждой итерации, построение графика в ОДНОМ окне, созданном plt.figure() выше
                plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
                plt.xlabel('Шаг сетки')
                plt.ylabel('Погрешность')
                plt.show()

