from ctypes.wintypes import DWORD
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 全局变量
δ = 1
τ = 0.1

# 微分方程
def func(dydt, t):
    dvdt,dxdt,dEdt,dRedt = dydt
    return np.array([
        F - (1/τ)

    ])