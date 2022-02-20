import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

c = 0.08
t右边界 = 10
STEP = 1000

def P(t):
    return np.sin(t) * np.sin(t) * np.log10(5 * t + 6) * np.exp( - t * t + 6 * t + 10) + 1

def f(t):
    return P(t)*np.exp(-c*x)

y = []
for i in range(STEP):
    x = i * (t右边界)/(STEP)
    积分,误差 = quad(f,0,x)
    y.append(np.exp(-c*x) * 积分)
plt.subplot(2,1,1)
plt.plot(np.linspace(0,t右边界,STEP),np.array(y))
plt.title('sum')

plt.subplot(2,1,2)
plt.plot(np.linspace(0,t右边界,STEP),P(np.linspace(0,t右边界,STEP)))
plt.title('P')
plt.show()