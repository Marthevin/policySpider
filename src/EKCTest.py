# -*- coding: utf-8 -*-
import numpy as np
from sklearn import linear_model
from sklearn import metrics
from matplotlib import pyplot as plt


cod = [505.1899,513.2950,517.3086,529.9742,548.9598,623.0631,589.4148,606.4762,621.8871,630.2357,618.0422,644.0468,650.8034,664.5134,667.9259,670.3798,608.6475,600.7107,611.3966,618.7483,617.6454,615.5796,622.1307,620.6532,621.3873]
tn =  [48.2837,49.9167,50.9293,53.7715,56.4865,69.9441,83.8769,69.3069,71.5017,73.5164,73.6489,75.4981,76.8754,78.9164,80.5273,82.5911,75.9318,75.3168,77.5027,79.2714,80.0658,80.4132,82.3450,82.7823,82.9376]
tp =  [458.1969,475.1002,483.4517,502.5145,526.1012,600.6423,582.4535,600.1656,620.0988,622.6316,623.2603,627.5690,633.0462,641.8904,659.1367,668.1303,614.4298,614.5946,624.5445,634.8056,638.8335,641.0104,650.0273,655.2358,652.5634]

agrgdp = [5017,5288.6,5800,6887.3,9471.4,12020,13877.8,14264.6,14618,14548.1,14716.2,15501.2,16188.6,16968.3,20901.8,21803.5,23313,27783,32747,34154,39354.6,46153.3,50892.7,58336.1,55321.7]#农业GDP数据
swrfzf = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]#水污染防治法从1996年实行
nyf =    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]#农业法从2002年实行
yhwj =   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]#2005年开始的中央一号文件
qua_agrdgp = [i*i for i in agrgdp]

X1= []

for i in range(len(agrgdp)):
    X1.append([qua_agrdgp[i],agrgdp[i]])
    
regr = linear_model.LinearRegression(fit_intercept=True,normalize=True)
regr.fit(X1,cod)

print regr.coef_
#y_predict = regr.predict(X1)
#mean_y = np.mean(cod)
#ESS = sum()
#RSS = sum()






