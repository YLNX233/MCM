import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from libs import *
#from codes.libs import *
from scipy.interpolate import make_interp_spline as spline
from scipy.signal import savgol_filter

EARTH_R = 6371.393
STEPS = 20000 # 地图中点的数目
eps = 0.0000001

'''
单位: 千米,小时,焦耳,瓦特
'''

class track:
    '''
    功能:计算赛道上关于路程的信息,并提供关于 dist 的查询
    初始化:输入一个numpy array,其第一行、第二行、第三行分别是纬度、经度、高度
    '''
    def __init__(self,route) -> None:
        self.y,self.x = self.longitudeLatitude_2_xy(route[0],route[1])
        self.y = self.y * 1000
        self.x = self.x * 1000
        self.height = route[2]
        self.n = self.x.size
        self.traverse_dist = 0
        self.d_list = [0]
        self.coordinate_2_dist()
        self.curvature = np.zeros(self.n)
        self.direction = np.zeros(self.n)
        self.grad = np.zeros(self.n)
        self.delta_dist = (self.traverse_dist)/(self.n)
        self.get_direction()
        self.xd=self.yd=self.heightd=self.curvatured=self.directiond = np.zeros(self.n)
        self.resample_by_dist()

    def longitudeLatitude_2_xy(self,latitude,longitude):
        latitude_km = (2 * np.pi * EARTH_R)/(360)
        latitude -= latitude.mean() # 中心化
        latitude = latitude*latitude_km

        longitude_km = (np.pi * EARTH_R * np.cos(latitude.mean()))/(180)
        longitude -= longitude.mean()
        longitude = longitude*longitude_km

        return latitude,longitude

    def coordinate_2_dist(self):
        for i in range(1,self.n):
            self.traverse_dist += np.sqrt((self.x[i]-self.x[i-1])**2 + (self.y[i]-self.y[i-1])**2)
            self.d_list.append(self.traverse_dist)
        self.d_list = np.array(self.d_list)
    
    def get_direction(self):
        # 首尾需要特判
        self.direction[0] = np.arctan2(self.y[1]-self.y[0],self.x[1]-self.x[0])
        self.direction[self.n - 1] = np.arctan2(self.y[self.n-1]-self.y[self.n-2],self.x[self.n-1]-self.x[self.n-2])
        
        for i in range(1,self.n-1):
            self.direction[i] = np.arctan2(self.y[i]-self.y[i-1],self.x[i]-self.x[i-1])
        

    def resample_by_dist(self):
        raw_index = self.d_list
        smooth_index = np.linspace(0,self.traverse_dist,STEPS)
        data = [self.x,self.y,self.height,self.curvature,self.direction]
        smoothed = []
        for iter in data:
            smoothed.append(spline(raw_index,iter)(smooth_index))

        self.xd,self.yd,self.heightd,self.curvatured,self.directiond = smoothed
        self.heightd = savgol_filter(self.heightd,101,1)
        self.curvatured = savgol_filter(self.curvatured,101,1)
        self.directiond = savgol_filter(self.curvatured,101,1)
        for i in range(1,self.n-1):
            self.grad[i] =(self.heightd[i+1] - self.heightd[i-1]) / (2*self.traverse_dist/self.n)
        self.grad = savgol_filter(self.grad,1001,1)
        # 卷积窗口
        
        #plt.plot((self.heightd - self.heightd.mean())/(self.heightd.max() - self.heightd.min()) ,c = 'red')
        #plt.plot(self.curvatured,c = 'blue')
        #plt.plot(self.directiond,c = 'black')
        #plt.plot(self.grad,c = 'black')
        #plt.plot(savgol_filter(self.grad,121,1))
        #plt.legend()
        #plt.show()

    def enquire(self,dist):
        idx = int((self.n * dist/self.traverse_dist))
        return self.heightd[idx],self.curvatured[idx],self.directiond[idx],self.grad[idx]

    def visualize_map(self,c = False):
        
        if c == True:
            plt.scatter(self.x,self.y,c=self.height,s=0.5)
        else:
            plt.scatter(self.x,self.y,c='red',s=3)
        #plt.colorbar()
        #plt.show()

'''
route = pd.read_csv('codes\maps\Hohhot.csv')
route = route.transpose().to_numpy()
route = resample(route,STEPS)
t = track(route)
t.visualize_map(True)
print(t.traverse_dist)
plt.show()
plt.fill_between(t.d_list, t.heightd, color='blue', alpha=0.3)
plt.xlabel('$distance \quad (m)$')
plt.ylabel('$elevation \quad (m)$')
plt.show()'''