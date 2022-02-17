from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv", header=0, sep=";")
columns = ['quality','fixed acidity', 'volatile acidity',
           'citric acid', 'residual sugar','chlorides', 
           'free sulfur dioxide', 'total sulfur dioxide', 
           'density','pH', 'sulphates', 'alcohol']
data = data[columns]
data.head()

class GraModel():
    '''灰色关联度分析模型'''
    def __init__(self,inputData,p=0.5,standard=True):
        '''
        初始化参数
        inputData：输入矩阵，纵轴为属性名，第一列为母序列
        p：分辨系数，范围0~1，一般取0.5，越小，关联系数间差异越大，区分能力越强
        standard：是否需要标准化
        '''
        self.inputData = np.array(inputData)
        self.p = p
        self.standard = standard
        #标准化
        self.standarOpt()
        #建模
        self.buildModel()
        
    def standarOpt(self):
        '''标准化输入数据'''
        if not self.standard:
            return None
        self.scaler = StandardScaler().fit(self.inputData) 
        self.inputData = self.scaler.transform(self.inputData)
        
    def buildModel(self):
        #第一列为母列，与其他列求绝对差
        momCol = self.inputData[:,0].copy()
        sonCol = self.inputData[:,0:].copy()
        for col in range(sonCol.shape[1]):
            sonCol[:,col] = abs(sonCol[:,col]-momCol)
        #求两级最小差和最大差
        minMin = sonCol.min()
        maxMax = sonCol.max()
        #计算关联系数矩阵
        cors = (minMin + self.p*maxMax)/(sonCol+self.p*maxMax)
        #求平均综合关联度
        meanCors = cors.mean(axis=0)
        self.result = {'cors':{'value':cors,'desc':'关联系数矩阵'},'meanCors':{'value':meanCors,'desc':'平均综合关联系数'}}

#建立灰色关联模型，标准化数据
model = GraModel(data,standard=True)
#模型计算结果
result = model.result
#平均关联程度
meanCors = result['meanCors']['value']
print(result)

#用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei'] 
#用来正常显示负号
plt.rcParams['axes.unicode_minus']=False
#可视化矩阵
sns.heatmap(meanCors.reshape(1,-1), square=True, annot=True,  cbar=False,
            vmax=1.0,
            linewidths=0.1,cmap='viridis')
plt.yticks([0,],['quality'])
plt.xticks(np.arange(0.5,12.5,1),columns,rotation=90)
plt.title('relevance')

plt.show()