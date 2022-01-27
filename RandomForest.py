# 随机森林
from argparse import Namespace
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

args = Namespace(
    seed = 2333,
    num_epochs=100,
    max_depth=4,
    min_samples_leaf=1,
    n_estimators=10
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
dtree = dtree.fit(X_train, Y_train) 

from six import StringIO  
from IPython.display import Image,display
from sklearn.tree import export_graphviz
import pydotplus

# 可解释性
dot_data = StringIO()
'''
with open("iris.dot", 'w') as f:
    f = dtree.export_graphviz(dtree, out_file=f)'''
export_graphviz(dtree, out_file=dot_data)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_pdf('test.pdf')