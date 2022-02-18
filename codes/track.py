import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import geotable as geo
# %% 全局变量
EARTH_R = 6371.393

# %% 转换地图数据为千米
def longitudeLatitude_2_xy(latitude,longitude):
    latitude_km = (2 * np.pi * EARTH_R)/(360)
    latitude -= latitude.mean() # 中心化
    latitude = latitude*latitude_km

    longitude_km = (np.pi * EARTH_R * np.cos(latitude.mean()))/(180)
    longitude -= longitude.mean()
    longitude = longitude*longitude_km

    return latitude,longitude

# %% 读取地图数据
route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
y,x = longitudeLatitude_2_xy(route[0],route[1])
h = route[2]

# %% 地图可视化
plt.scatter(x,y,c=h,s=0.5)
plt.colorbar()
plt.show()


