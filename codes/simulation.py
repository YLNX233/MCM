import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
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
    def __init__(self,args = [0, 12e-3, 20, 4.93, 55, 2403.5, 0.3, 3, 0.25, 0.2],wind_v = 0,wind_d = 0) -> None:
        self.Fa,    self.r,   self.P_max,     self.σ,       self.c_0,  self.E_t0, self.a, self.k, self.b, self.C_x = args # 
        '''疲劳度  恢复固有速率 无疲劳最大功率 固有能量提供速率 固有阻力系数  初始能量  最大加速度 C_R参数 C_R参数 空气阻力系数'''
        self.unamed = 7/11
        self.wind_v = wind_v
        self.wind_d = wind_d
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
        self.hlist = []
        self.P_act_last = (self.a+self.v/self.c_0)*self.v
    
    def wind(self):
    # 分别是风速、方向
        return self.wind_v,self.wind_d

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
        if(v_exp/self.v<2):
            self.v_e_list.append(v_exp)
        else:
            self.v_e_list.append(self.v)
        return (v_exp**2)/self.c_0*(self.E/1500)

    
    # 外因决策值
    def P_e(self):
        height,curvature,direction,grad = track.enquire(self.d)
        wind_spd,wind_direction = self.wind()
        C_R = self.k * grad + self.b

        # 注意： 这里的方向用的是x轴方位角
        direction = 1
        if(np.cos(direction - wind_direction)<0):
            direction = -1
        vec_len = np.sqrt(wind_spd**2 + self.v**2  - 2*wind_spd*self.v*np.cos(direction - wind_direction)) * direction
        return self.C_x * (1/2)*(vec_len**1) + C_R * self.v#np.cos(direction - wind_direction)

    def iteration(self,time):
        height,curvature,direction,grad = track.enquire(self.d)
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

        
        if time > 10 and P_act*0.6 > self.P_act_list[time - 2] :
            P_act = self.P_act_list[time - 2]
        
        self.P_act_list.append(P_act)   

        self.d = self.d + self.v*delta_t
        self.v =  self.v + self.acc(P_act,self.P_act_last,Pb)
        self.P_act_last = P_act
        self.E = self.E + self.delta_E(P_act)*delta_t
        self.SPact_e += (P_act*np.exp(self.r*time*delta_t)) * delta_t
        self.Fa = np.exp(-self.r*time*delta_t) * self.SPact_e
        self.hlist.append(height)

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

        plt.subplot(6,1,1)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.hlist,c = '#00cc5d')
        plt.ylabel('h (m)')
        plt.xlabel('d (m)')
        plt.xticks(size = 0)
        plt.subplot(6,1,2)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.E_list,c = '#00cc9f')
        plt.ylabel('E (J)')
        plt.xlabel('d (m)')
        plt.xticks(size = 0)
        plt.subplot(6,1,3)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.Fa_list,c = '#00cbc3')
        plt.ylabel('Fa (J)')
        plt.xlabel('d (m)')
        plt.xticks(size = 0)
        plt.subplot(6,1,4)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')        
        plt.plot(self.d_list,self.P_l_list,c = '#01b9cb')
        plt.plot(self.d_list,self.P_act_list,c = '#FDCB01')
        plt.legend(['$P_l$','$P_{act}$'],loc = 'right',frameon=False,bbox_to_anchor=(1.1, 0.5))
        plt.ylabel('P (W)')
        plt.xlabel('d (m)')
        plt.xticks(size = 0)
        plt.subplot(6,1,5)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.P_b_list,c = '#0061cc') 
        plt.ylabel('Pb (W)')
        plt.xlabel('d (m)')  
        plt.xticks(size = 0)      
        plt.subplot(6,1,6)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.P_e_list,c = '#001bfd')
        plt.ylabel('Pe (W)')
        plt.xlabel('d (m)')         
        plt.show()

    #def random_action

#两个选手对比图
参数们 = [0, 17e-3, 17, 5.4, 42, 2403.5, 0.3, 3, 0.25, 0.2]
s = simulation([0, 12e-3, 20, 4.93, 55, 2403.5, 0.3, 3, 0.25, 0.2])# 默认参数选手
s1 = simulation(args=参数们)#定制参数选手
T = s.sim_run()
s.graphing()
T1 = s1.sim_run()

plt.plot(s.d_list,s.P_act_list,c = '#70ab3e')
plt.plot(s1.d_list,s1.P_act_list,c = '#163760')
plt.legend(['$time \quad trail \quad specialist$','$Climber$'],loc = 'best',frameon=False)
plt.ylabel('$P_{act} \quad (W)$')
plt.xticks(np.arange(0,max(s.d_list),6000))
plt.show()
plt.fill_between(s.d_list,s.hlist, color='blue', alpha=0.3)
plt.ylabel('$Elevation \quad (m)$')
plt.xlabel('$d \quad (m)$')
plt.xticks(np.arange(0,max(s.d_list),6000))
print(T,T1)
plt.show()

'''
# 此处用于灵敏度分析
# 默认参数。对应关系可以看上面class __init__
args_defalut = [0, 12e-3, 20, 4.93, 55, 2403.5, 0.3, 3, 0.25, 0.2]
arg_list = []
t_list = []
num = 100

Z = np.zeros((10,10),dtype=float)

for X in range(-5,5,1):
    for Y in range(-5,5,1):
        L = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y,X)
        s = simulation(wind_v = L,wind_d = theta)
        Z[X,Y] = s.sim_run()

size=Z.shape
Y=np.arange(0,size[0],1)     
X=np.arange(0,size[1],1)

X,Y=np.meshgrid(X,Y)    
fig=plt.figure()
ax=fig.gca(projection='3d') 
ax.plot_surface(X-5,Y-5,Z,cmap='coolwarm')
plt.title('$T-wind \quad surface$',y = -5)
plt.show()'''
'''
for i in range(num):
    arg = 5 + (5)/num*i
    arg_list.append(arg)

    args_defalut[7] = arg

    s = simulation(args_defalut)
    t = s.sim_run()
    t_list.append(t)

t_list = np.array(t_list)
arg_list = np.array(arg_list)

t_list = spline(arg_list,t_list,k=2)(np.linspace(arg_list.min(),arg_list.max(),20000))
arg_list = np.linspace(arg_list.min(),arg_list.max(),20000)

plt.scatter(arg_list, t_list, c = t_list, cmap = 'coolwarm', zorder = 1 ,s = 0.4)
plt.title('$T-k \quad curve$',y = 0)
plt.show()
'''