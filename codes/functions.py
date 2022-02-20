import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import track as tk
from libs import *
Fa = 0 # 疲劳度
r = 10 # 恢复固有速率
P_max = 200 # 无疲劳最大功率
σ = 100 # 固有能量提供速率  !!单位为J/min!!
c_0 = 0.01 #固有阻力系数
E_t0 = 1000 # 初始能量
a = 1.54*10e4 # 最大加速度
k = 1 # C_R参数
b = 0 # C_R参数
C_x = 1 # 空气阻力系数

ms2kmh = 3.6

delta_t = 0.01 # 迭代时间

def wind():
    # 分别是风速、方向
    return 1,0

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
d = (v_exp0(track.traverse_dist)**2) / a
v = v_exp0(track.traverse_dist)

print(v_exp0(track.traverse_dist))

# 冲力
def f(P_act):
    global d,v,E,Fa
    return P_act/(v*ms2kmh)
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

# 内因决策值
def P_b():
    global d,v,E,Fa
    L_rem = track.traverse_dist - d
    delta = E**2 + 4 * ( (L_rem**2) * σ)/(L_rem/c_0)
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
    return C_x * (1/2)*(vec_len**3)*np.cos(np.abs(direction - wind_direction)) + C_R * v

P_s_list = []
P_act_list = []
def iteration():
    global d,v,E,Fa
    P_s = P_b()+P_e() # 决策函数返回值
    P_s_list.append(P_s)
    #print(P_b(),P_e(),P_l())
    P_act = min(P_s, P_l())
    P_act_list.append(P_act)
    
    d = d + v*delta_t
    v = v + delta_v(P_act)*delta_t
    E = E + delta_E(P_act)*delta_t
    Fa = Fa + delta_Fa(P_act)*delta_t


v_list = []
E_list = []
Fa_list = []
d_list = []

while d<track.traverse_dist:
    iteration()
    v_list.append(v)
    E_list.append(E)
    Fa_list.append(Fa)
    d_list.append(d)

plt.plot(v_list)
#plt.plot(E_list)
plt.show()
