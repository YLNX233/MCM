import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import seaborn as sns
import pandas as pd
import track as tk
from libs import *

track=delta_t = 0
import numpy as np


class simulation:
    def __init__(self,args = [0, 12e-3, 20, 4.93, 55, 2403.5, 0.3, 3, 0.25, 0.2],
    wind_v = 0,wind_d = 0,random = False) -> None:
        self.Fa,self.r,self.P_max,self.σ,self.c_0,self.E_t0,self.a,self.k,self.b,self.C_x=args 
        self.coefficient = 7/11
        self.wind_v = wind_v
        self.wind_d = wind_d

        '''variables being integrated'''
        self.E = self.E_t0
        self.d = (self.v_exp0(track.traverse_dist)**2) / self.a
        self.v = self.v_exp0(track.traverse_dist)
        self.SPact_e = 0

        '''Replay lists'''
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

        '''config'''
        self.random = random
    
    def wind(self):
        return self.wind_v,self.wind_d

    def v_exp0(self,L_rem):
        delta = self.E_t0**2 + 4 *self.coefficient* ((L_rem**2)*self.σ)/self.c_0
        return (self.E_t0 + np.sqrt(delta))/(2*(L_rem/self.c_0))

    def t1(self,v_exp0):
        return v_exp0/self.a


    # the upper bound of power output
    def P_l(self):
        return self.P_max * np.exp(-0.001*self.Fa)

    # the acceleration
    def acc(self,P_act,P_act_last,Pb):    
        return (P_act-P_act_last)/( (self.v/self.c_0)*(P_act/Pb) + 0.4*self.C_x * self.v)

    # the gradient of Energy
    def delta_E(self,P_act):
        if(self.E/2000 < 0.4) :
            return (self.σ - P_act)
        return (self.σ - P_act)

    # solution of power profile decision function based on physiological factors
    def P_b(self):
        L_rem = (track.traverse_dist - self.d)
        delta = self.E**2 + 4 *self.coefficient* (L_rem**2)*(self.σ)/self.c_0
        v_exp = (self.E + np.sqrt(delta)) / (2*(L_rem/self.c_0))
        if(v_exp/self.v<2):
            self.v_e_list.append(v_exp)
        else:
            self.v_e_list.append(self.v)
        return (v_exp**2)/self.c_0*(self.E/1500)**2

    
    # solution of power profile decision function based on environmental factors

    def P_e(self):
        height,curvature,direction,grad = track.enquire(self.d)
        wind_spd,wind_direction = self.wind()
        C_R = self.k * grad + self.b

        # Note: the direction used here is the X-axis azimuth
        vec_len =np.sqrt(wind_spd**2 + self.v**2-2*wind_spd*self.v*np.cos(direction-wind_direction))
        return self.C_x * (1/2)*(vec_len**1)*np.cos(direction - wind_direction) + C_R * self.v#

    def iteration(self,time):
        height,curvature,direction,grad = track.enquire(self.d)
        Pe = self.P_e()
        self.P_e_list.append(Pe)
        Pb = self.P_b()
        self.P_b_list.append(Pb*1.4)
        P_s = Pb + Pe # Actural power ooutput
        self.P_l_list.append(self.P_l())
        P_act = min(P_s, self.P_l()*(1+0.05)) # short periords of overloading are allowed
        if self.E<=0:
            P_act = self.σ*0.8# avoid negative E

        
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
        plt.subplot(6,1,2)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.E_list,c = '#00cc9f')
        plt.ylabel('E (J)')
        plt.xlabel('d (m)')
        plt.subplot(6,1,3)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.Fa_list,c = '#00cbc3')
        plt.ylabel('Fa (J)')
        plt.xlabel('d (m)')
        plt.subplot(6,1,4)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')        
        plt.plot(self.d_list,self.P_l_list,c = '#01b9cb')
        plt.plot(self.d_list,self.P_act_list,c = '#FDCB01')
        plt.legend(['$P_l$','$P_{act}$'],loc = 'right',frameon=False,bbox_to_anchor=(1.1, 0.5))
        plt.ylabel('P (W)')
        plt.xlabel('d (m)')
        plt.subplot(6,1,5)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.P_b_list,c = '#0061cc') 
        plt.ylabel('Pb (W)')
        plt.xlabel('d (m)')        
        plt.subplot(6,1,6)
        plt.grid(axis='x',color = '#cccccc')
        plt.grid(axis='y',color = '#cccccc')
        plt.plot(self.d_list,self.P_e_list,c = '#001bfd')
        plt.ylabel('Pe (W)')
        plt.xlabel('d (m)')         
        plt.show()

    def random_action(self,P_act):
        if self.random == False:
            return P_act
        else:
            return P_act*(1+np.random.randn()/10)