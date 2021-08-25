# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:20:21 2020

@author: ВАЛЕРИЙ
"""

from task2 import DerivativeNumCommon
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import sympy as smp
plt.rc('font', size=20)
import timeit
xSym = smp.Symbol('x')

h = 0.001

class LogisticRightHandSide:
        
    def __init__(self, alpha, R):
        self._alpha = float(alpha)
        self._R = float(R)
    
    
    def __call__(self, u):
        return self._alpha*u*(1. - u/self._R)
    
rhs1 = LogisticRightHandSide(alpha=0.2, R=100.)


class AbstractMethod:
    
    def __init__(self, f, u0, numBlocks, tStart, tEnd): # или задавать шаг dt?
        
        self.f = f
        self.u0 = u0
       
        self.numBlocks, self.numPoints = numBlocks, numBlocks + 1
        self.dt = (float(tEnd) - float(tStart))/float(numBlocks)
        
        self.solutionArray = np.zeros(self.numPoints)
        self.timeArray = np.linspace(tStart, tEnd, self.numPoints)
        
        self.tStart, self.tEnd = float(tStart), float(tEnd)
        
        
        print('Объект класса ' + self.__class__.__name__ + ' создан.')
        
  
    def Solve(self):
        
        print('Начало расчета методом %s ...' % self.__class__.__name__)
        start = timeit.default_timer()
        
        self.solutionArray[0] = self.u0
        
        # шаги по времени
        for i in range(self.numBlocks):
            
            # для краткости
            uOld, dt, f = self.solutionArray[i], self.dt, self.f
                                
            # формула явного метода Эйлера 
            self.solutionArray[i + 1] = self._AdvanceNextStep(i)
            
            # вывод на экран для отслеживания прогресса
            if ((i + 1) % (self.numBlocks//10) == 0):
                t = self.timeArray[i + 1]
                print('%.2f%% вычислений завершено' % (100.*float(t)/(self.tEnd - self.tStart)) )
                
            
            
        elapsedTime = float(timeit.default_timer() - start)
        print('Время расчета: %.2e сек.' % elapsedTime)
    
    ##### единственое отличие от предыдущей версии класса ################
    def _AdvanceNextStep(self, i):
        pass
    ##############################################################
    
    def PlotSolution(self):
        plt.plot(self.timeArray, self.solutionArray, '-o')
        plt.grid('off')
        plt.xlabel('Время')
        plt.ylabel('Популяция')
        #plt.show()
  
 
class ExplicitEuler_ver2(AbstractMethod):
    def _AdvanceNextStep(self, i):
        # для краткости
        uOld, dt, f = self.solutionArray[i], self.dt, self.f,  
        
        # формула явного метода Эйлера
        uNew = uOld + dt*f(uOld)
        
        return uNew
class SolveViaHeun(AbstractMethod):
    def _AdvanceNextStep(self, i):
        # для краткости
        uOld, dt, f = self.solutionArray[i], self.dt, self.f,  
        uStar = uOld + dt*f(uOld)
        uNew = uOld + dt/2. \
                            * (f(uOld) + f(uStar))
        return uNew 

      
class SolveViaRK4(AbstractMethod):
    def _AdvanceNextStep(self, i):
        uOld, dt, f = self.solutionArray[i], self.dt, self.f,  
        k1 = f(uOld)
        k2 = f(uOld + dt/2.*k1)
        k3 = f(uOld + dt/2.*k2)
        k4 = f(uOld + dt*k3)
        uNew = uOld + dt/6. * (k1 + 2.*k2 + 2.*k3 + k4)
        return uNew

   
class MethodTrapezium(AbstractMethod):
    def _AdvanceNextStep(self, i):
        uOld, dt, f = self.solutionArray[i], self.dt, self.f,  
        F = xSym - uOld - dt/2.*(f(xSym) + f(uOld))
        eF = smp.lambdify(xSym, F)
        derF = DerivativeNumCommon(eF, h)
        derF.SetA([0, 0, -0.5, 0, 0.5, 0, 0])
        u_null = uOld + dt*f(uOld)
        uk = u_null - eF(u_null)/derF(u_null)
        while np.fabs(eF(u_null)/derF(u_null)) > h :
            u_null = uk
            uk = u_null - eF(u_null)/derF(u_null)
            
        return uk
    
methodsClass = [ExplicitEuler_ver2, SolveViaHeun, SolveViaRK4, MethodTrapezium]
# именнно такая реализация в HPL
plt.figure(figsize=(11,7))
plt.title('Решения различными методоми ')
for methodClass in methodsClass:
    # вызываем конструктор
    method = methodClass(f=rhs1, u0=2., numBlocks=30, tStart=0., tEnd=80.)
    method.Solve()
    method.PlotSolution()

plt.show()

