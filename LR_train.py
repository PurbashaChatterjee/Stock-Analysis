'''
Created on Oct 15, 2017

@author: purbasha
'''
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
from datetime import timedelta, datetime
from math import log
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.metrics import classification_report

filename = 'VMShare/stocks-us-adjClose.csv'
csvfile = open(filename, 'rU')
stock = {}
filereader = pd.read_csv(csvfile, delimiter=",")
st_lst = []
stock = filereader.set_index('compiled from Yahoo! Finance data by Matt Borthwick').to_dict()

returnval = {}

def getStock():
    '''
    '''
    prevtime = datetime.today()
    prevprice = 0
    for key, val in stock.iteritems():
        returnval[key]={}
        for dt, price in val.iteritems():
            dt = datetime.strptime(dt, '%Y-%m-%d')
            timediff = dt - timedelta(1)
            if price > 0:
                if timediff==prevtime:
                    returnval[key][dt]=log(price)-log(prevprice)
                else: 
                    returnval[key][dt]=log(price)     
                prevprice = price   
                prevtime = dt 
    return returnval

#rel_df = pd.DataFrame.from_dict(dict([(k,Series(v)) for k,v in getStock().iteritems() ]))
#rel_df.to_csv('ReturnStocks.csv', header=True, sep='\t', encoding='utf-8')

rtnlst_train = []
data_1_train = []
VALIDATION_SPLIT = 0.15

req_dict={}
v = DictVectorizer(sparse=False)

def train():
    pos=0
    neg=0
    for key, val in getStock().iteritems():
        for dt, price in val.iteritems():   
            if price > 0 :
                rtnval = 1
                pos+=1
                rtnlst_train.append(rtnval)
                data_1_train.append((key,dt))                
            else:
                rtnlst_train.append(0)
                neg+=1
                data_1_train.append((key,dt))
    print pos,neg
    return rtnlst_train,data_1_train

labels, data = train()                     
perm = np.random.permutation(len(data))
idx_train = perm[:int(len(data)*(1-VALIDATION_SPLIT))]
idx_val = perm[int(len(data)*(1-VALIDATION_SPLIT)):]
print len(idx_train), len(idx_val)
ki=0
data_train = []
labels_train = []
i = 0.1
for idx in idx_train:
    labels_train.append(labels[idx])
    t = str(data[idx][1])
    date_object = datetime.strptime(t, '%Y-%m-%d %H:%M:%S') 
    w = date_object.strftime('%w')
    yr = date_object.strftime('%Y')
    mon = date_object.strftime('%m')
    if data[idx][0] not in req_dict: 
        req_dict[data[idx][0]]=i
        i+=0.1 
    data_train.append((float(req_dict[data[idx][0]]),float(w), float(yr), float(mon)))
    ki+=1
data_train = np.asarray(data_train)
data_train.reshape(2713140,4)    
#df_train = pd.DataFrame(list(data_train))
#df_train.pivot(index=0, columns=[1,2])

data_val = []
labels_val = []
si = 0
for idx in idx_val:
    #data_val.append(data[idx])
    labels_val.append(labels[idx])
    t = str(data[idx][1])
    date_object = datetime.strptime(t, '%Y-%m-%d %H:%M:%S') 
    w = date_object.strftime('%w') 
    yr = date_object.strftime('%Y')
    mon = date_object.strftime('%m')
    if data[idx][0] not in req_dict: 
        req_dict[data[idx][0]]=i
        i+=0.1 
    data_val.append((float(req_dict[data[idx][0]]),float(w),float(yr),float(mon)))
    si+=1
data_val = np.asarray(data_val)
data_val.reshape(478790,4)
    
LogReg = LogisticRegression()
LogReg.fit(data_train, labels_train) 
y_pred = LogReg.predict(data_val)   

confusion_matrix = confusion_matrix(labels_val, y_pred)
print(classification_report(labels_val, y_pred))              
               
                
        
    
    
