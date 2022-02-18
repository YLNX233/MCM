import numpy as np
import numpy.linalg as LA
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline as spline

def PJcurvature(x,y):
    '''
    根据三个点的坐标计算曲率与方向角

    输入: 三个点的坐标
    输出: 曲率、方向角
    '''
    t_a = LA.norm([x[1]-x[0],y[1]-y[0]])
    t_b = LA.norm([x[2]-x[1],y[2]-y[1]])
    
    M = np.array([
        [1, -t_a, t_a**2],
        [1, 0,    0     ],
        [1,  t_b, t_b**2]
    ])

    a = np.matmul(LA.inv(M),x)
    b = np.matmul(LA.inv(M),y)

    kappa = 2*(a[2]*b[1]-b[2]*a[1])/(a[1]**2.+b[1]**2.)**(1.5)
    return kappa, [b[1],-a[1]]/np.sqrt(a[1]**2.+b[1]**2.)

def resample(data,steps):
    '''
    重新采样并平滑数据

    输入:需要重新采样array的list、采样点数
    输出:重新采样后的array的list
    '''
    smoothed = []
    for iter in data:
        raw_index = np.linspace(0,iter.size,iter.size)
        smooth_index = np.linspace(0,iter.size,steps)
        smoothed.append(spline(raw_index,iter)(smooth_index))
    return smoothed