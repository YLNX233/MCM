# 决策树
from argparse import Namespace
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
import pandas as pd

args = Namespace(
    seed = 2333,
    max_depth = 100,
    min_samples_leaf = 1
)


from sklearn.tree import DecisionTreeClassifier
# 初始化
dtree = DecisionTreeClassifier(criterion="entropy", random_state=args.seed, 
                               max_depth=args.max_depth, 
                               min_samples_leaf=args.min_samples_leaf)

df = np.random.randn(10,4)
X_train =  pd.DataFrame(df,dtype=float)
Y_train = pd.DataFrame([0,1,0,1,0,1,0,1,0,1],dtype=int)

# 训练
dtree.fit(X_train, Y_train) 


# 预测
pred_train = dtree.predict(np.random.randn(10,4))

print(pred_train)

precision, recall, F1, _ = precision_recall_fscore_support(Y_train, pred_train, average="binary")
print ("precision: {0:.2f}. recall: {1:.2f}, F1: {2:.2f}".format(precision, recall, F1))