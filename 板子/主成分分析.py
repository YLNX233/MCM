import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.datasets import make_blobs


# X为样本特征，Y为样本簇类别， 共1000个样本，每个样本3个特征，共4个簇
X, y = make_blobs(n_samples=10000, n_features=3, centers=[[3,3, 3], [0,0,0], [1,1,1], [2,2,2]], cluster_std=[0.2, 0.1, 0.2, 0.2], 
                  random_state =9)
pca = PCA(n_components=2)# 注：当n_components<1 时代表主成分的方差和所占的最小比例阈值，此时将会自动决定维数
pca.fit(X)

X_new = pca.transform(X)
#plt.scatter(X[:, 0], X[:, 1], X[:, 2],marker='o')
plt.scatter(X_new[:, 0], X_new[:, 1],marker='o')
plt.show()