from ctypes.wintypes import DWORD
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

delta_t = 1 # 1秒为模拟步长
dist_cur = 0
t = 0

v_cur = 0

def wind_func():
    return 0,0

def drag_func():
    pass

def acceleration_func(power,wind,env):
    h,curv,direc,grad = env
    pass

def iteration(dist_cur,track):
    h,curv,direc,grad = track.enquire(dist_cur)
    wind_direc,wind_spd = wind_func()

    dist_cur += v_cur*delta_t
    v_cur += acceleration_func()*delta_t