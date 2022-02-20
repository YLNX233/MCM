import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import track as tk
from libs import *

Fa = 0 # 疲劳度
r = 10 # 恢复固有速率
P_max = 50 # 无疲劳最大功率
σ = 41.5 # 固有能量提供速率
c_0 = 0.01 #固有阻力系数
E_t0 = 2403.5 # 初始能量
a = 1.5 # 最大加速度
k = 2 # C_R参数
b = 0.2 # C_R参数
P = 10e2
C_x = 0.0001 # 空气阻力系数

delta_t = 1 # 迭代时间

def wind():
    # 分别是风速、方向
    return 0,0

route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
route = resample(route,tk.STEPS)
track = tk.track(route)

# %% section 1

def v_exp0(L_rem):
    delta = E_t0**2 + 4 * ((L_rem**2)*σ)/c_0
    return (-E_t0 + np.sqrt(delta))/(2*(L_rem/c_0))

def t1(v_exp0):
    return v_exp0/a

# %% section 2

# 积分值
E = E_t0
d = 0 #(v_exp0(track.traverse_dist)**2) / a
v = v_exp0(track.traverse_dist)

print(v_exp0(track.traverse_dist))

# 冲力
def f(P_act):
    global d,v,E,Fa
    return P_act/(v)
# Fa变化率
def delta_Fa(P_act):
    global d,v,E,Fa
    return -r * Fa + P_act

# 实时功率上限
def P_l():
    global d,v,E,Fa
    return P_max * np.exp(-0.01*Fa)

# 速度变化率
def delta_v(P_act):
    global d,v,E,Fa
    return -v/c_0 + f(P_act)

# 能量变化率
def delta_E(P_act):
    global d,v,E,Fa
    return σ - f(P_act)*v
    #return σ - (v**2)/c_0

# 内因决策值
def P_b():
    global d,v,E,Fa
    L_rem = track.traverse_dist - d
    delta = E**2 + 4 * (L_rem**2)*σ/c_0
    v_exp = (-E + np.sqrt(delta)) / (2*(L_rem/c_0))
    return c_0 * (v_exp**2)

# 外因决策值
def P_e():
    global d,v,E,Fa
    height,curvature,direction,grad = track.enquire(d)
    wind_spd,wind_direction = wind()
    C_R = k * grad + b

    # 注意： 这里的方向用的是x轴方位角
    vec_len = np.sqrt(wind_spd**2 + v**2  - 2*wind_spd*v*np.cos(np.abs(direction - wind_direction)) )
    return C_x * (1/2)*(vec_len**3)*P*np.cos(np.abs(direction - wind_direction)) + C_R * v

P_s_list = []
P_act_list = []
P_b_list = []
P_e_list = []

def iteration():
    global d,v,E,Fa
    Pb = P_b()
    P_b_list.append(Pb)
    Pe = P_e()
    P_e_list.append(Pe)
    P_s = Pb+Pe # 决策函数返回值
    P_s_list.append(P_s)
    #print(P_b(),P_e(),P_l())
    P_act = min(P_s, P_l())
    P_act_list.append(P_act)

    d = d + v*delta_t
    v = max(0.001, v + delta_v(P_act)*delta_t)
    E = E + delta_E(P_act)*delta_t
    Fa = Fa + max(0,delta_Fa(P_act)*delta_t)


v_list = []
E_list = []
Fa_list = []
d_list = []

print(track.traverse_dist)

while d<track.traverse_dist:
    #print(d)
    iteration()
    v_list.append(v)
    E_list.append(E)
    Fa_list.append(Fa)
    d_list.append(d)

plt.subplot(3,2,1)
plt.plot(v_list)
plt.title('v_list')
plt.subplot(3,2,2)
plt.plot(E_list)
plt.title('E_list')

plt.subplot(3,2,3)
plt.plot(Fa_list)
plt.title('Fa_list')

plt.subplot(3,2,4)
plt.plot(P_s_list)
plt.plot(P_act_list)
plt.title('P_s_list')

plt.subplot(3,2,5)
plt.plot(P_b_list)
plt.title('Pb')

plt.subplot(3,2,6)
plt.plot(P_e_list)
plt.title('pe')

#plt.plot(E_list)
plt.show()
