import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import geotable as geo
from libs import *
# %% 全局变量
EARTH_R = 6371.393
STEPS = 10000 # 地图中点的数目

# %% 转换地图数据为千米
def longitudeLatitude_2_xy(latitude,longitude):
    latitude_km = (2 * np.pi * EARTH_R)/(360)
    latitude -= latitude.mean() # 中心化
    latitude = latitude*latitude_km

    longitude_km = (np.pi * EARTH_R * np.cos(latitude.mean()))/(180)
    longitude -= longitude.mean()
    longitude = longitude*longitude_km

    return latitude,longitude


# %% 计算出坡度、方向、曲率关于距离的函数
def coordinate_2_dist(x,y):
    n = x.size
    dist = 0
    for i in range(n):
        pass
    

# %% 读取地图数据
route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
y,x = longitudeLatitude_2_xy(route[0],route[1])
h = route[2]
plt.scatter(x,y,c='red',s=3)
y,x,h = resample([y,x,h])

coordinate_2_dist(x,y)
# %% 地图可视化
plt.scatter(x,y,c=h,s=0.5)
plt.colorbar()
plt.show()