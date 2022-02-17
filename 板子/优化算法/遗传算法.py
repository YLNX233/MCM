from turtle import color
from sko.GA import GA
import matplotlib.pyplot as plt
import pandas as pd
def f(x):
    x1, x2, x3 = x
    return x1 ** 2 + (x2 - 0.05) ** 2 + x3 ** 2

#2个变量，每代取50个，800次迭代，上下界及精度
ga = GA(func=f, n_dim=3, size_pop=50, max_iter=800, precision=1e-7)
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)

fig, ax = plt.subplots(2, 1)
ax[0].plot(ga.all_history_Y, '.', color = 'blue')
pd.DataFrame(ga.all_history_Y).min(axis=1).cummin().plot(kind='line')
plt.show()