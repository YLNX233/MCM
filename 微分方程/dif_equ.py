# 计算微分方程的数值解，使用scipy的odeint函数
# 高阶方程需要转化为多个一阶微分方程
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def diff_eg(y_list, x, a, b):
    """
    y_list是所有在一阶微分方程组中的变量
    需要定义的y_list对应的微分方程组，也是以一个list的形式
    a,b等参数将在odint中自动传入args的内容
    """
    theta, omega = y_list
    dydt = [omega, -a*omega - b*np.sin(theta)]
    return dydt

# x 求解范围        
x = np.linspace(0, 10, 100)  # 给出x范围

# 微分方程组本组
def func(dydt, t, g, l):
	dθdt,dωdt = dydt
    #此处定义一阶微分方程组如dθdt = dωdt等
    #顺序与上面的对应
	return np.array([dωdt,-g/l*dθdt])

# 求数值解的自变量.此处顺便限定了起点/终点/步长
t = np.linspace(0, 20, 2000)
#y的初值
y0 = [0, 35/180*np.pi]
# args 参数，顺序需与func中的对应
args = (9.8,1)

"""
odint在给定的t下，以y0为初值，计算func微分方程组在参数args下的结果
结果是一个是一个矩阵，每一个因变量一列，顺序如函数中所定义
"""
result = odeint(func=func, y0=y0, t=t, args = args)# 添加args = 来向微分方程传递参数，或者干脆全局

# 绘图
plt.plot(t, result[:, 0])  # ω-t曲线
plt.plot(t, result[:, 1])  # θ-t曲线
plt.show()