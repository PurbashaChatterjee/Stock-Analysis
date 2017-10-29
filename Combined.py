'''
Created on Oct 29, 2017

@author: purbasha
'''

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pandas as pd
from datetime import timedelta, datetime
from math import log
import numpy as np
from sklearn.metrics import classification_report

filename = 'VMShare/stocks-us-adjClose.csv'
file_open = 'VMShare/stocks-us-moreData/stocks-us-adjOpen.csv'
csvfile = open(filename, 'rU')
csvfile2 = open(file_open, 'rU')
stock = {}
filereader = pd.read_csv(csvfile, delimiter=",")
file_open = pd.read_csv(csvfile2, delimiter=",")
stock = filereader.set_index('compiled from Yahoo! Finance data by Matt Borthwick').to_dict()
stock_open = file_open.set_index('compiled from Yahoo! Finance data by Matt Borthwick').to_dict()
returnval = {}

def getStock():
    '''
    '''
    prevtime = datetime.today()
    prevprice = 0
    for (key, val), (k2,v2) in zip(stock.iteritems(), stock_open.iteritems()):
        returnval[key]={}
        if key==k2:
            for (dt, price), (d2, open) in zip(val.iteritems(), v2.iteritems()):
                dt = datetime.strptime(dt, '%Y-%m-%d')
                timediff = dt - timedelta(1)
                if price > 0:
                    if timediff==prevtime:
                        retn = log(price)-log(prevprice)
                        returnval[key][dt]= (retn,price, open)
                    else: 
                        returnval[key][dt]=(log(price),price, open)     
                    prevprice = price   
                    prevtime = dt 
    return returnval

rtnlst_train = []
data_1_train = []
VALIDATION_SPLIT = 0.15

req_dict={}

def train():
    pos=0
    neg=0
    for key, val in getStock().iteritems():
        for dt, ret_price in val.iteritems(): 
            retn, price, open =  ret_price 
            if retn > 0 :
                rtnval = 2
                pos+=1
                rtnlst_train.append(rtnval)
                data_1_train.append((key,dt, price, open))                
            else:
                rtnlst_train.append(1)
                neg+=1
                data_1_train.append((key,dt, price, open))
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
    data_train.append((float(req_dict[data[idx][0]]),float(data[idx][2]),float(data[idx][3]),float(w), float(yr), float(mon)))
    ki+=1
data_train = np.asarray(data_train)
data_train.reshape(2713140,6)    

data_val = []
labels_val = []
si = 0
for idx in idx_val:
    labels_val.append(labels[idx])
    t = str(data[idx][1])
    date_object = datetime.strptime(t, '%Y-%m-%d %H:%M:%S') 
    w = date_object.strftime('%w') 
    yr = date_object.strftime('%Y')
    mon = date_object.strftime('%m')
    if data[idx][0] not in req_dict: 
        req_dict[data[idx][0]]=i
        i+=0.1 
    data_val.append((float(req_dict[data[idx][0]]),float(data[idx][2]),float(data[idx][3]),float(w),float(yr),float(mon)))
    si+=1
data_val = np.asarray(data_val)
data_val.reshape(478790,6)

def logisticReg():    
    LogReg = LogisticRegression()
    LogReg.fit(data_train, labels_train) 
    y_pred = LogReg.predict(data_val)       
    print(classification_report(labels_val, y_pred))              
               
def randomFor():
    """
    Random Forest Binary Classification
    """
    clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1)
    print "RF data fit"
    clf.fit(data_train, labels_train) 
    print "RF label predict" 
    y_pred = clf.predict(data_val)  
    print "RF data score"  
    accuracy = clf.score(data_val, labels_val)    
    print accuracy                
    print(classification_report(labels_val, y_pred))                  

def SVM():
    clf = SVC()
    print "SVM data fit"
    clf.fit(data_train, labels_train)  
    print "SVM label predict" 
    y_pred = clf.predict(data_val)    
    #accuracy = clf.score(data_val, labels_val)   
    #print accuracy
    print(classification_report(labels_val, y_pred))    
     
print("After applying Logistic Regression--")
logisticReg()
print("After applying SVM Classifier")
SVM()    
