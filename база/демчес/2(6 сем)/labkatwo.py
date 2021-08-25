# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:49:58 2020

@author: ВАЛЕРИЙ
"""

from numpy import sin, cos, exp, sqrt, linspace
import matplotlib.pyplot as plt


x0 = 1/sqrt(5)
u0 = 1
u1 = 2


def ka(x):
    return sin(x) * sin(x) + 1

def kb(x):
    return sin(x) * sin(x) + 1

def qa(x):
    return x

def qb(x):
    return x**3

def fa(x):
    return 1

def fb(x):
    return x * x - 1

# константы для аналитического решения
def cs(l1, l2):
    a11 = exp(-l1*x0)-exp(l1*x0)
    a12 = exp(l2*(2-x0))-exp(l2*x0)
    a21 = ka(x0)*l1*(exp(l1*x0)+exp(-l1*x0))
    a22 = kb(x0)*l2*(exp(l2*(2-x0))+exp(l2*x0))
    ma = fa(x0)/qa(x0)
    mb = fb(x0)/qb(x0)
    b1 = mb-ma+(ma-u0)*exp(l1*x0)-(mb-u1)*exp(l2*(1-x0))
    b2 = ka(x0)*l1*(u0-ma)*exp(l1*x0)+kb(x0)*l2*(u1-mb)*exp(l2*(1-x0))
    c1 = (((u0-ma)*a11-b1)*a22-((u0-ma)*a21-b2)*a12)/(a11*a22-a12*a21)
    c2 = (b1*a22-b2*a12)/(a11*a22-a12*a21)
    c3 = (b2*a11-b1*a21)/(a11*a22-a12*a21)
    c4 = (u1-mb)*exp(l2)-c3*exp(2*l2)
    return c1, c2, c3, c4


def model_u(x, l_1, l_2, c_1, c_2, c_3, c_4):
    if x < x0:
        c1 = c_1
        c2 = c_2
        m = fa(x0)/qa(x0)
        l1 = l_1
    else:
        c1 = c_3
        c2 = c_4
        m = fb(x0)/qb(x0)
        l1 = l_2
    return c1 * exp(l1 * x) + c2 * exp(-l1 * x) + m


def counter_sweep_method(a, b, c, d, la, lb):
    n = len(a)
    alpha = [0] * (n-1)
    alpha[1] = -a[1]/b[1]
    alpha[-1] = -c[-1]/b[-1]
    beta = [0] * (n-1)
    beta[1] = (d[1]-c[1]*u0)/b[1]
    beta[-1] = (d[-1]-c[-1]*u1)/b[-1]
    x = [u0] * n
    x[-1] = u1
    for i in range(2, la):
        alpha[i] = (-a[i]/(c[i]*alpha[i-1]+b[i]))
        beta[i] = ((d[i]-c[i]*beta[i-1])/(b[i]+c[i]*alpha[i-1]))
    for i in reversed(range(lb+1, n-2)):
        alpha[i] = -c[i]/(b[i]+a[i]*alpha[i+1])
        beta[i] = (d[i]-a[i]*beta[i+1])/(b[i]+a[i]*alpha[i+1])
    x[lb] = x[la] = (ka(x0)*beta[la-1]+kb(x0)*beta[lb+1])/(ka(x0)*(1-alpha[la-1])+kb(x0)*(1-alpha[lb+1]))
    for i in reversed(range(1, la)):
        x[i] = alpha[i]*x[i+1]+beta[i]
    for i in range(lb+1, n-1):
        x[i] = alpha[i]*x[i-1]+beta[i]
    return x


def init_const_abcd(n):
    a, b, c, d = [], [], [], []
    for i in range(n):
        a.append(ka(x0) if i < la else kb(x0))
        b.append(-2 * ka(x0) - qa(x0) * h ** 2 if i < la else -2 * kb(x0) - qb(x0) * h ** 2)
        c.append(ka(x0) if i < la else kb(x0))
        d.append(-fa(x0) * h ** 2 if i < la else -fb(x0) * h ** 2)
    return a, b, c, d


def init_variable_abcd(n):
    a, b, c, d = [], [], [], []
    for i in range(n):
        a.append(ka(h * (i + 1. / 2)) if i < la else kb(h * (i + 1. / 2)))
        b.append(-(ka(h * (i + 1. / 2)) + ka(h * (i - 1. / 2)) + qa(h * i) * h ** 2) if i < la else -(
        kb(h * (i + 1. / 2)) + kb(h * (i - 1. / 2)) + qb(h * i) * h ** 2))
        c.append(ka(h * (i - 1. / 2)) if i < la else kb(h * (i - 1. / 2)))
        d.append(-fa(h * i) * h ** 2 if i < la else -fb(h * i) * h ** 2)
    return a, b, c, d


def u_model_comp(n):
    a, b, c, d = init_const_abcd(n)
    x = counter_sweep_method(a, b, c, d, la, lb)
    return [x[int(i*(n-1)/10)] for i in range(11)]


def u_var_comp(n):
    a, b, c, d = init_variable_abcd(n)
    x = counter_sweep_method(a, b, c, d, la, lb)
    return [x[int(i*(n-1)/10)] for i in range(11)]


slot = [0, 1]
rep_x = linspace(slot[0], slot[1], 11)
n = 81921
h = (slot[1] - slot[0]) / (n-1)

print("x:        ", " ".join("%.6E" % x for x in rep_x))
l1 = sqrt(qa(x0)/ka(x0))
l2 = sqrt(qb(x0)/kb(x0))
c1, c2, c3, c4 = cs(l1, l2)

u_model_analit = [model_u(x, l1, l2, c1, c2, c3, c4) for x in rep_x]
print("u_analit: ", " ".join("%.6E" % i for i in u_model_analit))
la = int(x0/h)
lb = la+1
plt.plot(rep_x, u_model_analit, color="green")

u_model_c = u_model_comp(n)
plt.plot(rep_x, u_model_c, color="blue")
print("u_m_comp: ", " ".join("%.6E" % i for i in u_model_c))

print("diff:     ", " ".join("%.6E" % abs(i-j) for i,j in zip(u_model_analit, u_model_c)))
print("max diff: ", "%.6E" % max(abs(i-j) for i,j in zip(u_model_analit, u_model_c)))

xs = u_var_comp(n)
plt.plot(rep_x, xs, color="yellow")
print("u_comp:   ", " ".join("%.6E" % i for i in xs))
plt.axis([0, 1, 0, 2])
plt.show()
