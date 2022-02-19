import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from libs import *
#from codes.libs import *
from scipy.interpolate import make_interp_spline as spline

EARTH_R = 6371.393
STEPS = 10000 # 地图中点的数目
eps = 0.0000001

class track:
    '''
    功能:计算赛道上关于路程的信息,并提供关于 dist 的查询
    初始化:输入一个numpy array,其第一行、第二行、第三行分别是纬度、经度、高度
    '''
    def __init__(self,route) -> None:
        self.y,self.x = self.longitudeLatitude_2_xy(route[0],route[1])
        self.height = route[2]
        self.n = self.x.size
        self.traverse_dist = 0
        self.d_list = [0]
        self.coordinate_2_dist()
        self.curvature = np.zeros(self.n)
        self.direction = np.zeros(self.n)
        self.get_curvature_direction()
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
            self.traverse_dist += (self.x[i]-self.x[i-1])**2 + (self.y[i]-self.y[i-1])**2
            self.d_list.append(self.traverse_dist)
        self.d_list = np.array(self.d_list)
    
    def get_curvature_direction(self):
        # 首尾需要特判
        vec = 0
        self.curvature[0],vec = PJcurvature(np.array([self.x[0]+eps,self.x[0],self.x[1]]),np.array([self.y[0]+eps,self.y[0],self.y[1]]))
        self.direction[0] = np.arctan2(vec[0],vec[1])
        self.curvature[self.n-1],vec = PJcurvature(np.array([self.x[self.n-2],self.x[self.n-1],self.x[self.n-1]+eps]),
                                                            np.array([self.y[self.n-2],self.y[self.n-1],self.y[self.n-1]+eps]))
        self.direction[self.n-1] = np.arctan2(vec[0],vec[1])
        
        for i in range(1,self.n-1):
            self.curvature[i],vec = PJcurvature(self.x[i-1:i+2],self.y[i-1:i+2])
            if(np.abs(self.curvature[i]>100)):
                self.curvature[i] = self.curvature[i-1]
            self.direction[i] = np.arctan2(vec[0],vec[1])

        #plt.plot(self.curvature)
        #plt.plot(self.direction)
        #plt.show()
        

    def resample_by_dist(self):
        raw_index = self.d_list
        smooth_index = np.linspace(0,self.traverse_dist,STEPS)
        data = [self.x,self.y,self.height,self.curvature,self.direction]
        smoothed = []
        for iter in data:
            smoothed.append(spline(raw_index,iter)(smooth_index))

        self.xd,self.yd,self.heightd,self.curvatured,self.directiond = smoothed

        #plt.plot(self.heightd,c = 'red')
        #plt.plot(self.curvatured,c = 'blue')
        #plt.plot(self.directiond,c = 'black')
        #plt.legend()
        #plt.show()

    def enquire(self,dist):
        idx = int((self.n * dist/self.traverse_dist))
        return self.heightd[idx],self.curvatured[idx],self.directiond[idx]

    def visualize_map(self,c = False):
        if c == True:
            plt.scatter(self.x,self.y,c=self.height,s=0.5)
        else:
            plt.scatter(self.x,self.y,c='red',s=3)
        plt.colorbar()
        #plt.show()
    

route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
t0 = track(route)
route = resample(route,10000)
t = track(route)
t.visualize_map(True)
t0.visualize_map(False)
plt.show()