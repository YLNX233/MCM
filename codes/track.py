import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import geotable as geo

route = pd.read_csv('codes\maps\Tokyo.csv')
route = route.transpose().to_numpy()
print(route)
plt.scatter(x = route[0],y = route[1],c=route[2])
plt.colorbar()
plt.show()

