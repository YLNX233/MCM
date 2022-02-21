from cmath import e
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import track as tk
from libs import *

route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
route = resample(route,tk.STEPS)
track = tk.track(route)

delta_t = 1 # 迭代时间

class simulation:
    def __init__(self,args = [0, 12e-3, 20, 4.93, 55, 2403.5, 0.3, 3, 0.25, 0.2]) -> None:
        self.Fa,    self.r,   self.P_max,     self.σ,       self.c_0,  self.E_t0, self.a, self.k, self.b, self.C_x = args # 
        '''疲劳度  恢复固有速率 无疲劳最大功率 固有能量提供速率 固有阻力系数  初始能量  最大加速度 C_R参数 C_R参数 空气阻力系数'''
        self.unamed = 7/11
        '''参数1'''

        '''被积分的变量们'''
        self.E = self.E_t0
        self.d = (self.v_exp0(track.traverse_dist)**2) / self.a
        self.v = self.v_exp0(track.traverse_dist)
        self.SPact_e = 0

        '''记忆单元'''
        self.v_e_list = []
        self.P_l_list = []
        self.P_act_list = []
        self.P_b_list = []
        self.P_e_list = []
        self.v_list = []
        self.E_list = []
        self.Fa_list = []
        self.d_list = []
        self.P_act_last = (self.a+self.v/self.c_0)*self.v
    
    def wind(self):
    # 分别是风速、方向
        return 0,0

    def v_exp0(self,L_rem):
        delta = self.E_t0**2 + 4 *self.unamed* ((L_rem**2)*self.σ)/self.c_0
        return (self.E_t0 + np.sqrt(delta))/(2*(L_rem/self.c_0))

    def t1(self,v_exp0):
        return v_exp0/self.a


    # 实时功率上限
    def P_l(self):
        return self.P_max * np.exp(-0.001*self.Fa)

    # 速度变化率
    def acc(self,P_act,P_act_last,Pb):    
        return (P_act-P_act_last)/( (self.v/self.c_0)*(P_act/Pb) + 0.4*self.C_x * self.v)#min(-(Pe/v)+(P_act/v),a)#

    # 能量变化率
    def delta_E(self,P_act):
        if(self.E/2000 < 0.4) :
            return (self.σ - P_act)
        return (self.σ/(self.E/1500) - P_act) #* np.sqrt(1-(E/E_t0))
        #return σ - (v**2)/c_0


    # 内因决策值
    def P_b(self):
        L_rem = (track.traverse_dist - self.d)
        delta = self.E**2 + 4 *self.unamed* (L_rem**2)*(self.σ)/self.c_0
        v_exp = (self.E + np.sqrt(delta)) / (2*(L_rem/self.c_0))
        self.v_e_list.append(v_exp)
        return (v_exp**2)/self.c_0*(self.E/1500)

    
    # 外因决策值
    def P_e(self):
        height,curvature,direction,grad = track.enquire(self.d)
        wind_spd,wind_direction = self.wind()
        C_R = self.k * grad + self.b

        # 注意： 这里的方向用的是x轴方位角
        vec_len = np.sqrt(wind_spd**2 + self.v**2  - 2*wind_spd*self.v*np.cos(np.abs(direction - wind_direction)) )
        return self.C_x * (1/2)*(vec_len**1) + C_R * self.v#*np.cos(np.abs(direction - wind_direction))

    def iteration(self,time):
        Pe = self.P_e()
        self.P_e_list.append(Pe)
        Pb = self.P_b()
        self.P_b_list.append(Pb*1.4)
        P_s = Pb + Pe # 决策函数返回值
        self.P_l_list.append(self.P_l())
        #print(P_b(),P_e(),P_l())
        P_act = min(P_s, self.P_l()*(1+0.05))
        #P_act = P_s
        if self.E<=0:
            P_act = self.σ*0.8
        self.P_act_list.append(P_act+1)
        self.d = self.d + self.v*delta_t
        self.v =  self.v + self.acc(P_act,self.P_act_last,Pb)
        self.P_act_last = P_act
        self.E = self.E + self.delta_E(P_act)*delta_t
        self.SPact_e += (P_act*np.exp(self.r*time*delta_t)) * delta_t
        self.Fa = np.exp(-self.r*time*delta_t) * self.SPact_e

    def sim_run(self):
        time = 0
        while self.d<track.traverse_dist:
            self.iteration(time)
            self.v_list.append(self.v)
            self.E_list.append(self.E)
            self.Fa_list.append(self.Fa)
            self.d_list.append(self.d)
            time += delta_t
        return time

    def graphing(self):
        plt.grid(axis='x')
        plt.plot(self.d_list,self.v_list)
        plt.xticks(size = 0)
        #plt.plot(v_e_list)
        plt.title('$v-d$',loc = 'right',y=0)
        
        plt.subplot(6,1,2)
        plt.grid(axis='x',color = '#cccccc')
        plt.plot(self.d_list,self.E_list)
        plt.title('$E_{rem}-d$',loc = 'right',y=0)
        plt.xticks(size = 0) 

        plt.subplot(6,1,3)
        plt.grid(axis='x',color = '#cccccc')
        plt.plot(self.d_list,self.Fa_list)
        plt.title('$FA-d$',loc = 'right',y=0)
        plt.xticks(size = 0) 

        plt.subplot(6,1,4)
        plt.grid(axis='x',color = '#cccccc')
        plt.plot(self.d_list,self.P_l_list)
        plt.plot(self.d_list,self.P_act_list)
        plt.title('$P_s-d$',loc = 'right',y=0)
        plt.xticks(size = 0) 

        plt.subplot(6,1,5)
        plt.grid(axis='x',color = '#cccccc')
        plt.plot(self.d_list,self.P_b_list)
        plt.title('$P_b-d$',loc = 'right',y=0)
        plt.xticks(size = 0) 

        plt.subplot(6,1,6)
        plt.grid(axis='x',color = '#cccccc')
        plt.plot(self.d_list,self.P_e_list)
        plt.title('$P_e-d$',loc = 'right',y=0)




args_defalut = [0, 12e-3, 20, 4.93, 55, 2403.5, 0.3, 3, 0.25, 0.2]
arg_list = []
t_list = []
for i in range(100):
    σ = 2.8+(4)/100*i
    arg_list.append(σ)

    args_defalut[3] = σ

    s = simulation(args_defalut)
    t = s.sim_run()
    t_list.append(t)

print(arg_list)
print(t_list)
plt.plot(arg_list,t_list,c = 'blue')
plt.show()
    