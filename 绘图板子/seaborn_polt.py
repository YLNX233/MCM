# seaborn画图板子 http://seaborn.pydata.org/examples/index.html
import seaborn as sns
import matplotlib.pyplot as plt

'''通用内容'''
# 图主题
themes = ['white','dark','whitegrid','darkgrid','ticks']
sns.set_theme(style=themes[2])
# 调色板
cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)



'''带点权散点图'''
planets = sns.load_dataset("planets")
g = sns.relplot(
    data=planets,
    # x轴，y轴，hue = 颜色， size = 点大小，palette = 调色板， sizes = 点尺寸范围
    x="distance", y="orbital_period",
    hue="year", size="mass",
    palette=cmap, sizes=(10, 200),
)

'''坐标属性'''
g.set(xscale="log", yscale="log")
g.ax.xaxis.grid(True, "minor", linewidth=.25)
g.ax.yaxis.grid(True, "minor", linewidth=.25)
g.despine(left=True, bottom=True)
plt.show()