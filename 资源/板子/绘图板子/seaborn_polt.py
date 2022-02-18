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
g0 = sns.relplot(
    data=planets,
    # x轴，y轴，hue = 颜色， size = 点大小，palette = 调色板， sizes = 点尺寸范围
    x="distance", y="orbital_period",
    hue="year", size="mass",
    palette=cmap, sizes=(10, 200),
)

'''时序图（带误差带）
fmri = sns.load_dataset("fmri")
# x轴，y轴，hue = 颜色， size = 点大小，palette = 调色板， sizes = 点尺寸范围
g1 = sns.lineplot(x="timepoint", y="signal",
             hue="region", style="event",
             data=fmri)

sns.relplot(
    data=dots,
    x="time", y="firing_rate",
    hue="coherence", size="choice", col="align",
    kind="line", size_order=["T1", "T2"], palette=palette,
    height=5, aspect=.75, facet_kws=dict(sharex=False),
)'''

'''坐标属性
g0.set(xscale="log", yscale="log")
g0.ax.xaxis.grid(True, "minor", linewidth=.25)
g0.ax.yaxis.grid(True, "minor", linewidth=.25)
g0.despine(left=True, bottom=True)'''
plt.show()