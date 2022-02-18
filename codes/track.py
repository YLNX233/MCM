import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from codes.libs import *

EARTH_R = 6371.393
STEPS = 10000 # 地图中点的数目

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
        self.curvature = []
        self.direction = []

    def longitudeLatitude_2_xy(latitude,longitude):
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
    
    def get_curvature_direction(self):
        pass

    def resample_by_dist(self):
        pass

    def enquire(self,dist):
        pass

    def visualize_map(self):
        plt.scatter(self.x,self.y,c=self.height,s=0.5)
        plt.colorbar()
        plt.show()
    

route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()

t = track(route)