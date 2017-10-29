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
        meanStock=val
        prevtime=time[0]
        lst=[]
         
    else:
        for i in range(0,710):
            meanStock[i]=val[i]
            lst.append((meanStock[i], filereader.columns[i+1]))
            prevtime=time[0]
        yearly[time[0]]=lst  

def year_max():  
    v=list(yearly.values())
    k=list(yearly.keys())
    return k[v[0].index(max(v[0]))]

maxstock = {}

for sKeys,sVals in yearly.iteritems():
    m = max(i for i in sVals)
    print sKeys, m


stock2 = filereader.set_index('compiled from Yahoo! Finance data by Matt Borthwick').to_dict('list')
#print stock2['SJW']

day = {}  
meanStock = 0      
for key, val in stock.iteritems():
        for i in range(0,710):
            if val[i] > 0: 
                meanStock+=float(val[i])
        day[key]=meanStock/(710) 

lists = sorted(day.items()) # sorted by key, return a list of tuples
x, y = zip(*lists) # unpack a list of pairs into two tuples
               
        

    