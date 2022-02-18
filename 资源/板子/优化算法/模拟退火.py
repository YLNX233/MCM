from sko.SA import SA
import matplotlib.pyplot as plt
import pandas as pd

# 定义需要最优化的f
def f(x):
    x1, x2, x3 = x
    return x1 ** 2 + (x2 - 0.05) ** 2 + x3 ** 2

# 还有SAFast，SABoltzmann（玻尔兹曼），SACauchy（柯西）
# 还有自带的SA_TSP，用于解决旅行商问题
sa = SA(func=f, x0=[1, 1, 1], T_max=1, T_min=1e-9, L=300, max_stay_counter=150)
x_star, y_star = sa.run()
print(x_star, y_star)

plt.plot(sa.best_y_history)
plt.show()