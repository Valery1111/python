# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 12:56:18 2020

@author: ВАЛЕРИЙ
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sympy as smp
plt.rc('font', size=20)
import timeit
xSym = smp.Symbol('x')



class AbstractMethod:
    
    def __init__(self, u0, kappa, ab, numBlocks, tStart, tEnd):
        
        self.k, self.a, self.b = kappa, ab[0], ab[1]
        self.numBlocks, self.numPoints = numBlocks, numBlocks + 1
        self.h = (float(ab[1]) - float(ab[0]))/float(numBlocks)
        self.dt = (self.h ** 2) / (200 * kappa)
        self.solutionArray = np.zeros(self.numPoints)
        for i in range(self.numPoints):
            if i * self.h >= u0[0] and i * self.h <= u0[1]:
                self.solutionArray[i] = 1 
            else:
                self.solutionArray[i] = 0
        self.NextsolutionArray = np.zeros(self.numPoints)
        self.X = np.linspace(ab[0], ab[1], self.numPoints)
        self.tStart, self.tEnd = float(tStart), float(tEnd)
        self.f = lambda s: (s[2:self.numPoints] - 2*s[1:self.numPoints-1] + s[:self.numPoints-2])
        
        
        print('Объект класса ' + self.__class__.__name__ + ' создан.')
        
  
    def Solve(self):
        
        print('Начало расчета методом %s ...' % self.__class__.__name__)
        start = timeit.default_timer()
        
        while self.tStart < self.tEnd:
            uOld, dt, f = self.solutionArray, self.dt, self.f
            self.NextsolutionArray[1:self.numPoints-1] = self._AdvanceNextStep()
            self.NextsolutionArray[0] = 0
            self.NextsolutionArray[-1] = 0
            self.solutionArray = self.NextsolutionArray
            self.tStart += dt
            
        elapsedTime = float(timeit.default_timer() - start)
        print('Время расчета: %.2e сек.' % elapsedTime)
    
    ##### единственое отличие от предыдущей версии класса ################
    def _AdvanceNextStep(self):
        pass
    ##############################################################
    
    def PlotSolution(self):
        plt.plot(self.X, self.solutionArray, '-o')
        plt.grid('off')
        plt.show()
  
 
class ExplicitEuler_ver2(AbstractMethod):
    def _AdvanceNextStep(self):
        # для краткости
        uOld, dt, f = self.solutionArray, self.dt, self.f,  
        
        # формула явного метода Эйлера
        uNew = uOld[1:self.numPoints-1] + dt * self.k * f(uOld) / (self.h*self.h)
        return uNew
   
class SolveViaHeun(AbstractMethod):
    def _AdvanceNextStep(self):
        # для краткости
        uOld, dt, f = self.solutionArray, self.dt, self.f
        uStar = np.zeros(self.numPoints)
        uStar[1:self.numPoints-1] = uOld[1:self.numPoints-1] + dt * self.k * f(uOld) / (self.h*self.h)
        uStar[0] = 0
        uStar[-1] = 0
        uNew = uOld[1:self.numPoints-1] + dt * self.k * (f(uOld+uStar)) / (2*self.h*self.h) 
        
        return uNew 

     
class SolveViaRK4(AbstractMethod):
    def _AdvanceNextStep(self):
        uOld, dt, f = self.solutionArray, self.dt, self.f  
        k1, k2, k3, k4 = np.zeros(self.numPoints - 2),np.zeros(self.numPoints),np.zeros(self.numPoints),np.zeros(self.numPoints)
        dtt = dt * self.k / (self.h*self.h)
        k1 = f(uOld)
        kk1 = np.zeros(self.numPoints)
        kk1[1:self.numPoints-1] = k1
        k2 = f(uOld + dtt/2.*kk1)
        kk2 = np.zeros(self.numPoints)
        kk2[1:self.numPoints-1] = k2
        k3 = f(uOld + dtt/2.*kk2)
        kk3 = np.zeros(self.numPoints)
        kk3[1:self.numPoints-1] = k3
        k4 = f(uOld + dtt*kk3)
        
        uNew = uOld[1:self.numPoints-1] + dtt/6. * (k1 + 2.*k2 + 2.*k3 + k4)
        return uNew

 
methodsClass = [ExplicitEuler_ver2, SolveViaHeun, SolveViaRK4]#, MethodTrapezium]
# именнно такая реализация в HPL
plt.figure(figsize=(11,7))
plt.title('Решения различными методоми ')
for methodClass in methodsClass:
    # вызываем конструктор
    method = methodClass([0.4, 0.6], 0.1, [0, 1], numBlocks=25, tStart=0., tEnd=0.04)
    method.Solve()
    method.PlotSolution()
    

