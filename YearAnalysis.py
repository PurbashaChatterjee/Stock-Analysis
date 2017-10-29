'''
Created on Oct 15, 2017

@author: purbasha
'''

import matplotlib.pyplot as plt
import pandas as pd

filename = 'VMShare/stocks-us-adjClose.csv'
csvfile = open(filename, 'rU')
stock = {}
filereader = pd.read_csv(csvfile, delimiter=",")
st_lst = []
stock = filereader.set_index('compiled from Yahoo! Finance data by Matt Borthwick').T.to_dict('list')
yearly = {}
prevtime=''

for key, val in stock.iteritems():
    time = key.split('-')
    lst=[]
    if not time[0]==prevtime:
        if not val[0] > 0:
            meanStock=val[0]
        else:
            meanStock=0   
        prevtime=time[0]
        lst=[]
        j=1
         
    else:
        for i in range(0,710):
            if val[i] > 0:
                meanStock+=float(val[i])
            prevtime=time[0]
        j+=1
        yearly[time[0]]=meanStock/(j*710) 

print yearly        

lists = sorted(yearly.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.show()


    
        
        
        
        