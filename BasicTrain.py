'''
Created on Oct 15, 2017

@author: purbasha
'''
import pandas as pd
from datetime import datetime, timedelta
from math import log
import matplotlib.pyplot as plt


filename = 'VMShare/stocks-us-adjClose.csv'
csvfile = open(filename, 'rU')
stock = {}
filereader = pd.read_csv(csvfile, delimiter=",")
st_lst = []
stock = filereader.set_index('compiled from Yahoo! Finance data by Matt Borthwick').to_dict()

returnval = {}

def getStock():
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

analysis = getStock()['SJW']
lists = sorted(analysis.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

#plt.plot(x, y)
#plt.show()

dtreturn = {}
for key, val in stock.iteritems():
    for k,v in val.iteritems():
        dt = datetime.strptime(k, '%Y-%m-%d')
        if k in dtreturn:
            dtreturn[dt]+=v
        else:
            dtreturn[dt]=v
            
lists1 = sorted(dtreturn.items()) # sorted by key, return a list of tuples

x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples

plt.plot(x1, y1)
plt.show()    
    
    