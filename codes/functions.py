import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import track as tk
from libs import *

Fa = 0 # 疲劳度
r = 10e-3 # 恢复固有速率
P_max = 20 # 无疲劳最大功率
σ = 3.5 # 固有能量提供速率
c_0 = 55 #固有阻力系数
E_t0 = 2000 # 初始能量
a = 0.3 # 最大加速度
k = 3 # C_R参数
b = 0.25 # C_R参数
C_x = 0.2 # 空气阻力系数

unamed = 1

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
    delta = E_t0**2 + 4 *unamed* ((L_rem**2)*σ)/c_0
    return (E_t0 + np.sqrt(delta))/(2*(L_rem/c_0))

def t1(v_exp0):
    return v_exp0/a

# %% section 2

# 积分值
E = E_t0
d = (v_exp0(track.traverse_dist)**2) / a
v = v_exp0(track.traverse_dist)

#print(v)

'''
# Fa变化率
def delta_Fa(P_act):
    global d,v,E,Fa
    return -r * Fa + P_act
'''

# 实时功率上限
def P_l():
    global d,v,E,Fa
    return P_max * np.exp(-0.1*Fa)

# 速度变化率
def acc(P_act,P_act_last,Pb):
    global d,v,E,Fa
    return (P_act-P_act_last)/( (v/c_0)*(P_act/Pb) )#min(-(Pe/v)+(P_act/v),a)#

# 能量变化率
def delta_E(P_act):
    global d,v,E,Fa
    return (σ - P_act) #* np.sqrt(1-(E/E_t0))
    #return σ - (v**2)/c_0

v_e_list = []

# 内因决策值
def P_b():
    global d,v,E,Fa
    L_rem = (track.traverse_dist - d)
    delta = E**2 + 4 *unamed* (L_rem**2)*(σ)/c_0
    v_exp = (E + np.sqrt(delta)) / (2*(L_rem/c_0))
    v_e_list.append(v_exp)
    #if(v_exp<v):
    return (v_exp**2)/c_0
    #else:
        #return 1.05 * c_0 * (v_exp**2)

    
# 外因决策值
def P_e():
    global d,v,E,Fa
    height,curvature,direction,grad = track.enquire(d)
    wind_spd,wind_direction = wind()
    C_R = k * 0.01 + b

    # 注意： 这里的方向用的是x轴方位角
    vec_len = np.sqrt(wind_spd**2 + v**2  - 2*wind_spd*v*np.cos(np.abs(direction - wind_direction)) )
    return C_x * (1/2)*(vec_len**1) + C_R * v#*np.cos(np.abs(direction - wind_direction))

P_l_list = []
P_act_list = []
P_b_list = []
P_e_list = []
P_act_last = (a+v/c_0)*v

SPact_e = 0

def iteration(time):
    global d,v,E,Fa,P_act_last,SPact_e
    Pe = P_e()
    P_e_list.append(Pe)
    Pb = P_b()
    P_b_list.append(Pb)
    P_s = Pb+Pe # 决策函数返回值
    P_l_list.append(P_l())
    #print(P_b(),P_e(),P_l())
    P_act = min(P_s, P_l())
    if E<=0:
        P_act = σ*0.8
    P_act_list.append(P_act)

    d = d + v*delta_t
    #print(d)    
    print(P_act,P_act_last,Pb,Pe,acc(P_act,P_act_last,Pb),v)
    v =  v + acc(P_act,P_act_last,Pb)

    
    P_act_last = P_act
    #v = vexp(Pe)
    #print(v)
    E = E + delta_E(P_act)*delta_t
    SPact_e += (P_act*np.exp(-r*time*delta_t)) * delta_t
    Fa = np.exp(-r*time*delta_t) * SPact_e
    #Fa = Fa + delta_Fa(P_act)*delta_t

    


v_list = []
E_list = []
Fa_list = []
d_list = []

print(v)
print(track.traverse_dist)

time = 0
#plt.ion()
#while d<track.traverse_dist:
for i in range(20):
    #print(d)
    iteration(time)
    v_list.append(v)
    E_list.append(E)
    Fa_list.append(Fa)
    d_list.append(d)

    plt.subplot(3,2,1)
    plt.plot(v_list)
    plt.plot(v_e_list)
    plt.title('v_list')
    plt.subplot(3,2,2)
    plt.plot(E_list)
    plt.title('E_list')

    plt.subplot(3,2,3)
    plt.plot(Fa_list)
    plt.title('Fa_list')

    plt.subplot(3,2,4)
    plt.plot(P_l_list)
    plt.plot(P_act_list)
    plt.title('P_s_list')

    plt.subplot(3,2,5)
    plt.plot(P_b_list)
    plt.title('Pb')

    plt.subplot(3,2,6)
    plt.plot(P_e_list)
    plt.title('pe')

    #plt.pause(1)

    time += delta_t

#plt.plot(E_list)
#plt.show()
