from ctypes.wintypes import DWORD
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import track as tk
Fa = 0 # 疲劳度
r = 100 # 恢复固有速率
P_max = 2000 # 无疲劳最大功率
σ = 100 # 固有能量提供速率  !!单位为J/min!!
c_0 = 1 #固有阻力系数
E_t0 = 100000 # 初始能量
a = 1.54*10e4 # 最大加速度
k = 1 # C_R参数
b = 0 # C_R参数
C_x = 1 # 空气阻力系数

delta_t = 0.1 # 迭代时间

def wind():
    # 分别是风速、方向
    return 1,0

route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
track = tk(route)
# %% section 1

def v_exp0(L_rem):
    delta = E_t0**2 - 4 * (L_rem*σ)/c_0
    v = (-E_t0 + np.sqrt(delta))/(2*(1/c_0))

    return v

def t1(v_exp0,):
    return v_exp0/a

# %% section 2

# 积分值
E = E_t0
d = (v_exp0(track.traverse_dist)**2) / a
v = v_exp0(track.traverse_dist)

# 冲力
def f(P_act):
    return P_act/v
# Fa变化率
def delta_Fa(P_act):
    return -r * Fa + P_act

# 实时功率上限
def P_l():
    return P_max * np.exp(-Fa)

# 速度变化率
def delta_v(P_act):
    return v/c_0 - f(P_act)

# 能量变化率
def delta_E(P_act):
    return σ - f(P_act)*v

# 内因决策值
def P_b():
    delta = E**2 - 4 * ((track.traverse_dist - d)*σ)/c_0
    v_exp = (-E + np.sqrt(delta))/(2*(1/c_0))
    return c_0 * (v_exp**2)

# 外因决策值
def P_e():
    height,curvature,direction,grad = track.enquire(d)
    wind_spd,wind_direction = wind()
    C_R = k * (grad/v) + b

    # 注意： 这里的方向用的是x轴方位角
    vec_len = np.sqrt(wind_spd**2 + v**2  - 2*wind_spd*v*np.cos(np.abs(direction - wind_direction)) )
    return C_x * (1/2)*(vec_len**3)*np.cos(np.abs(direction - wind_direction)) + C_R * v

def iteration():
    P_s = P_b()+P_e() # 决策函数返回值
    P_act = np.min(P_s, P_l())
    d += v*delta_t
    v += delta_v(P_act)*delta_t
    E += delta_E(P_act)*delta_t
    Fa += delta_Fa(P_act)*delta_t


v_list = []
while d<track.traverse_dist:
    iteration()
    v_list.append(v)

plt.plot(v_list)
plt.show()
