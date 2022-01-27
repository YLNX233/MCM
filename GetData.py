from argparse import Namespace
import numpy as np
import pandas as pd
import urllib.request

NULL = 0

class TaitanNike():
    def __init__(self) -> None:
        self.data = NULL
        self.trainData = NULL
        self.testData = NULL
        self.file = "titanic.csv"
        self.url = "..."
        self.useless = ["name", "cabin", "ticket"]
        self.trainSize = 0.8
        self.Y = "survived"

    # 下载数据集
    def download(self,fromNet = False):
        if fromNet:
            response = urllib.request.urlopen(self.url)
            html = response.read()
            with open(self.file, 'wb') as f:
                f.write(html)
                
        df = pd.read_csv(self.file, header=0)
        df.head()
        self.data = df

    # 去掉无用\无效的数据
    def dropUseless(self):
        self.data = self.data.dropna()
        return self.data.drop(self.useless, axis=1)

    # 把文字信息转为数字
    def Str2Dig(self):
        self.data['sex'] = self.data['sex'].map( {'female': 0, 'male': 1} ).astype(int)
        self.data["embarked"] = self.data['embarked'].dropna().map( {'S':0, 'C':1, 'Q':2} ).astype(int)
        return self.data

    # 分为训练集、数据集
    def batching(self):
        mask = np.random.rand(len(self.data)) < self.trainSize
        train = self.data[mask]
        test = self.data[~mask]
        print ("Train size: {0}, test size: {1}".format(len(train), len(test)))
        self.trainData,self.testData = train,test

    # 将特征与结果分开
    def sepXY(self,df):
        return df.drop([self.Y], axis=1),df[self.Y]

    def AutoPrepare(self):
        self.download()
        self.dropUseless()
        self.Str2Dig()
        self.batching()

d = TaitanNike()
d.AutoPrepare()

print(d.trainData)