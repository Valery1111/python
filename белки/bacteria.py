# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:55:40 2020

@author: ВАЛЕРИЙ
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import random


k, c = 2, 0
a, b = 20, 20
fig = plt.figure()
ax = plt.axes(xlim=(0, a), ylim=(-b, b))
xr, yr = a/2, 0
quantity = 10
death = 0
line, = ax.plot([], [], lw=1, marker='o', color="white", markerfacecolor="red")#

def init():
        line.set_data([], [])
        return line,
    
iks, igrik = [], []
ex, ey = [], []
    
for bac in range(quantity):
    #line, = ax.plot([], [], lw=1)#
    x0 = random.uniform(0, a)
    y0 = random.uniform(-b, b)
    R = (x0 - xr) * (x0 - xr) + (y0 - yr) * (y0 - yr)
    iks, igrik = [], []

    if x0 < xr:
        c0 = k * x0
    else:
        c0 = -k * (x0 - a)

    r = 0.5
    
    for i in range(1000):
        fi = random.uniform(0, 6.28)
        ix = x0 + r * np.cos(fi)
        iks.append(ix)
        iy = y0 + r * np.sin(fi)
        igrik.append(iy)
        
        if ix <= 0 or ix >= a:
            for j in range(1000 - i):
                iks.append(0)
                igrik.append(0)
            death += 1
            break
        '''
        if ix < a/2:
            c = k * ix
        else:
            c = -k * (ix - a)
    
        if c < c0:
            r += 0.01
        else:
            r -= 0.01    
        ''' 
        R1 = (ix - xr) * (ix - xr) + (iy - yr) * (iy - yr)
        if R < R1:
            r += 0.01
        else:
            r -= 0.01
        
        if R1 >= (xr * xr * 1.4):
            for j in range(1000 - i):
                iks.append(0)
                igrik.append(0)
            death += 1
            break
        R = R1     
        
        c0 = c
        x0, y0 = ix, iy
    ex.append(iks)
    ey.append(igrik)
    #line.set_data(iks, igrik)#
grx, gry = [], []

#
for i in range(1000):
    xx, yy = [], []
    for bac in range(quantity):
        xx.append(ex[bac][i])
        yy.append(ey[bac][i])
    grx.append(xx)
    gry.append(yy)

def animate(i):
    line.set_data(grx[i], gry[i])
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=100, blit=True)

plt.show()
print('смерти:', death)
