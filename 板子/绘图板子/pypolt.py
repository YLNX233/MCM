# pypolt画图板子
import matplotlib.pyplot as plt
import numpy as np
from math import sin
from plotdf import plotdf

NY = 100
NX = 100
xmin,xmax = [-10,10]
ymin,ymax = [-14,14]
dy = (ymax -ymin )/(NY-1.)
dx = (xmax -xmin)/(NX-1.)

def f(x,g=1,l=1,m=1,b=1):
    return np.array([x[1],-g*sin(x[0])/l-b*x[1]/m/l])

# print(plt.style.available)
# 双变量微分方程相图
plt.style.use('seaborn-deep')# 主题可以改一改，虽然还是有点丑

# 特定解
plotdf(f, # 微分方程。定义如上，所有自变量打包在一个x里面
    np.array([xmin,xmax]), # [xmin,xmax]
    np.array([ymin,ymax]),# [ymin,ymax]
    [(1.05,-9),(0,5),(-1.05,9)], # 微分方程初值，这会产生一个解并在图像上画出一条对应的曲线
    parameters={"g":9.8,"l":0.5,"m":0.3,"b":0.05},# 输进函数f的参数
    gridsteps= 0, # 梯度矢量场标箭头的密度
    nsteps=10000) # 计算一组解的总步数
plt.legend(['a','b','c'])

# 梯度矢量场
y = np.array([ ymin + float(i)*dy for i in range(NY)])
x = np.array([ xmin + float(i)*dx for i in range(NX)])
x, y = np.meshgrid( x, y, indexing = 'xy', sparse = False)

u = y
v = -9.8*np.sin(x)/0.5 - 0.05*x/0.3/0.5
color = np.sqrt(u**2 + v**2) # 颜色

plt.quiver(x, y, u, v, color,) # 箭头
plt.streamplot(x, y, u, v, color=color,linewidth=v/10) # 流

plt.colorbar()

plt.show()