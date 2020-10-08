from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import datetime as dt
import numpy as np
import re
#import seaborn as sns
#import matplotlib.pyplot as plt
#from statsmodels.tsa.stattools import acf, pacf
import pandas_datareader.data as getSymbols
from dateutil.relativedelta import relativedelta
#import statsmodels.api as sm
#import tensorflow as tf
#from  tensorflow import keras as kr
#print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
import scipy
#sns.set_style('darkgrid')
#sns.mpl.rc('figure',figsize=(10, 5))


# set up folder and file names and paths
wikiComps = "./data/sp500Members.csv"
wikiChngs = "./data/sp500Changes.csv"
inpName = './data/inp.pkl'
tgtName = './data/tgt.pkl'
cleanDataName = './data/cleanData.pkl'
cleanDataName2 = './data/cleanData2.pkl'

# scrape the S&P 500 components from the wiki page
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#Selected_changes_to_the_list_of_S&P_500_components' 
response = requests.get(url)
print(response.status_code)
soup = BeautifulSoup(response.text,"html.parser")
table = soup.findAll('table',{"class":"sortable"})[0]
tr = table.findAll(['tr'])[1::]
csvFile = open(wikiComps,'wt',newline='', encoding='utf-8')
writer = csv.writer(csvFile)  
try:   
        for cell in tr:
            th = cell.find_all('th')
            th_data = [col.text.strip('\n') for col in th]
            td = cell.find_all('td')
            row = [i.text.replace('\n','') for i in td]
            writer.writerow(th_data+row)      
        
finally:   
    csvFile.close()

# scrape the changes in S&P 500 components from the wiki page
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#Selected_changes_to_the_list_of_S&P_500_components' 
response = requests.get(url)
print(response.status_code)
soup = BeautifulSoup(response.text,"html.parser")
table = soup.findAll('table',{"class":"sortable"})[1]
tr = table.findAll(['tr'])[2::]
csvFile = open(wikiChngs,'wt',newline='', encoding='utf-8')
writer = csv.writer(csvFile)  
try:   
        for cell in tr:
            th = cell.find_all('th')
            th_data = [col.text.strip('\n') for col in th]
            td = cell.find_all('td')
            row = [i.text.replace('\n','') for i in td]
            writer.writerow(th_data+row)      
        
finally:   
    csvFile.close()

# load in the data into dataframes
sp500MemberCols = ['Symbol', 'Security', 'SEC filings', 'GICS Sector', 'GICS Sub Industry', 'Headquarter Location', 'Date first added', 'CIK', 'Founded']
sp500ChangeCols = ['Date', 'Added Ticker', 'Added Security', 'Removed Ticker', 'Removed Security', 'Reason']
dfMem = pd.read_csv(wikiComps, header=None, names=sp500MemberCols)
dfChng = pd.read_csv(wikiChngs, header=None, names=sp500ChangeCols)

# replace '.' characters with '-' characters
def fixSym(sym):
    if isinstance(sym, str):
        if '.' in sym:
            return '-'.join(sym.split('.'))
    return sym

dfMem['Symbol'] = dfMem['Symbol'].apply(fixSym).values
dfChng['Added Ticker'] = dfChng['Added Ticker'].apply(fixSym).values
dfChng['Removed Ticker'] = dfChng['Removed Ticker'].apply(fixSym).values

# change date columns to datetime object
dfChng['Date'] = pd.to_datetime(dfChng['Date'])
dfChng = dfChng.sort_values(['Date'], ascending=False)
#dfChng

# work with data only after 2014
dfChng = dfChng[dfChng['Date'] >= dt.datetime(2019,6,30)]
#dfChng

# construct list of symbols for each data
symbols = []
startDates = []
allDates = dfChng['Date'].unique()
curSymbols = dfMem['Symbol'].to_list()
for date in allDates:
    symbols.append(curSymbols)
    startDates.append(date)
    subDf = dfChng[ dfChng['Date'] == date]
    subAdd = subDf['Added Ticker'].dropna()
    subRmv = subDf['Removed Ticker'].dropna()
    print("date is {}".format(date))
    if len(subAdd) != 0:
        for i in subAdd.values:
            print("Removing {}".format(i))
            if i == 'UA':
                if date == dt.datetime(2016,4,8):
                    curSymbols.remove('UAA')
            elif i == 'LLL':
                curSymbols.remove('LHX')
            elif i == 'RHT':
                curSymbols.remove('IBM')
            elif i == 'APC':
                curSymbols.remove('OXY')
            elif i == 'TSS':
                curSymbols.remove('GPN')
            elif i == 'CELG':
                curSymbols.remove('BMY')
            elif i == 'VIAB':
                curSymbols.remove('VIAC')
            elif i == 'WCG':
                curSymbols.remove('CNC')
            elif i == 'ARNC':
                curSymbols.remove('HWM')
            elif i == 'Q':
                curSymbols.remove('IQV')
            elif i == 'BMS':
                curSymbols.remove('AMCR')
            elif i == 'GDI':
                curSymbols.remove('IR')
            else:
                curSymbols.remove(i)
    if len(subRmv) != 0:
        for i in subRmv.values:
            print("Adding {}".format(i))
            if i == 'UA':
                if date == dt.datetime(2016,4,8):
                    curSymbols.append('UAA')
            elif i == 'LLL':
                curSymbols.append('LHX')
            elif i == 'RHT':
                curSymbols.append('IBM')
            elif i == 'APC':
                curSymbols.append('OXY')
            elif i == 'TSS':
                curSymbols.append('GPN')
            elif i == 'CELG':
                curSymbols.append('BMY')
            elif i == 'VIAB':
                curSymbols.append('VIAC')
            elif i == 'WCG':
                curSymbols.append('CNC')
            elif i == 'ARNC':
                curSymbols.append('HWM')
            elif i == 'Q':
                curSymbols.append('IQV')
            elif i == 'BMS':
                curSymbols.append('AMCR')
            elif i == 'GDI':
                curSymbols.append('IR')
            else:
                curSymbols.append(i)
        
len(startDates)
len(symbols)

# get the first and last dates
firstEndDate = dt.datetime(2020,9,29)
endDates = list()
endDates.append(np.datetime64(firstEndDate))
endDates.extend(startDates)
endDates = endDates[:-1]
#endDates

len(endDates)

# get a list of all the symbols
allSymbols = np.array(curSymbols)
allSymbols = allSymbols.flatten()
allSymbols = pd.unique(allSymbols)
allSymbols = allSymbols.tolist()

# scrape the stock stats from Yahoo Finance
for curSym in allSymbols[allSymbols.index('USB')::]:
#for curSym in allSymbols:
    curUrl = "https://finance.yahoo.com/quote/" + curSym + "/key-statistics?p=" + curSym
    response = requests.get(curUrl)
    #if (allSymbols.index(curSym)+1) % 10 == 0:
    print("working {} out of {}: ".format(allSymbols.index(curSym)+1, len(allSymbols), curSym))
    soup = BeautifulSoup(response.text,"html.parser")
    table = soup.find('table')
    tr = table.findAll(['tr'])
    csvFile = open("./data/" + curSym + "-Stats.csv",'wt',newline='', encoding='utf-8')
    writer = csv.writer(csvFile)  
    try:   
            for cell in tr:
                th = cell.find_all('th')
                th_data = [col.text.strip('\n') for col in th]
                td = cell.find_all('td')
                row = [i.text.replace('\n','') for i in td]
                writer.writerow(th_data+row)      

    finally:   
        csvFile.close()
#allSymbols

# get the price data for stocks from Yahoo Finance API, 
# and concat it with scrapped Yahoo stats  data
#inp = []
#tgt = []
cleanData = []
#for curSym in allSymbols[allSymbols.index('APC')::]:
#for curSym in allSymbols[490::]:
for curSym in allSymbols:
    #if (allSymbols.index(curSym)+1) % 10 == 0:
    print("working on {} of {}: {}".format(allSymbols.index(curSym)+1,len(allSymbols),curSym))
    # step 1: 
    # getting prices from yahoo
    curData = getSymbols.DataReader(curSym, 'yahoo', start=dt.datetime(2019,6,30),end=endDates[0])
    #curData
    # step 2:
    # adding a column for the symbol
    curData['Symbol'] = curSym
    #curData
    # step 3:
    # adding a column for number of days since last record
    curData['DateDelta'] = [ x.days for x in curData.reset_index().Date.diff()] 
    # curData
    # step 4: 
    # adding a column for the return (difference in the log) of the data
    curData['Return'] = np.log(curData['Adj Close']).diff()
    #curData
    # step 4.2: 
    # adding a column for the future return (difference in the log) of the data
    curData['FutureReturn'] = curData['Return'].shift(-1)
    #curData
    # step 4.3: 
    # adding a column for the future price of the data
    curData['FuturePrice'] = curData['Adj Close'].shift(-1)
    #curData
    # step 5:
    # adding a column for return. which is the Raw Return divided by n Days since last record
    curData['HighLow'] = curData['High'] / curData['Low']
    #curData
    # step 6:
    # resetting the index
    curData = curData.reset_index()
    #curData
    # step 7:
    # loading the df of scrapped stats
    curStats = pd.read_csv("./data/" + curSym + "-Stats.csv", index_col=0) 
    curStats = curStats[curStats.columns[1::]].T
    curStats = curStats.reset_index()
    curStats[curStats.columns[0]] = pd.to_datetime(curStats[curStats.columns[0]])
    curStats.rename(columns={'index':'Date'}, inplace=True)
    curStats = curStats.sort_values(curStats.columns[0]).set_index(curStats.columns[0]).reset_index()
    #curStats
    # step 8:
    # merging the price data with the scraped data, sorting by date
    testMerge = curData.merge(curStats, how='outer', on='Date')
    testMerge = testMerge.sort_values(['Date']).set_index(['Date'])
    #testMerge
    # step 9:
    # forward filling the stats columns
    startColIndex = testMerge.columns.to_list().index('Market Cap (intraday) 5')
    testMerge[testMerge.columns[startColIndex::]] = testMerge[testMerge.columns[startColIndex::]].fillna(method='ffill')
    #testMerge
    # step 10:
    # removing all rows that don't have price data
    testMerge.dropna(subset=['High'],inplace=True)
    testMerge.dropna(subset=['Return'],inplace=True)
    testMerge.dropna(subset=['FutureReturn'],inplace=True)
    #testMerge
    # step 11:
    # taking the log of volume
    #testMerge['Volume'] = np.log(testMerge['Volume'])
    #testMerge
    # step 12:
    # deleting columns not needed
    del testMerge['High'], testMerge['Low'], testMerge['Open'], testMerge['Close']
    #testMerge
    # step 13: 
    # resetting index
    # step 14:
    #inp.append(testMerge.shift().reset_index())
    #tgt.append(testMerge.reset_index())
    cleanData.append(testMerge.reset_index())

#inp = pd.concat(inp, ignore_index=True)
#tgt = pd.concat(tgt, ignore_index=True)
cleanData = pd.concat(cleanData, ignore_index=True)
#inp.to_pickle(inpName)
#tgt.to_pickle(tgtName)
cleanData.to_pickle(cleanDataName)

# load the clean data file
cleanData = pd.read_pickle(cleanDataName)
#cleanData

# define the sections of the data based on stats dates from yahoo finance
sections = [dt.datetime(2019, 9, 30),
 dt.datetime(2019, 12, 31),
 dt.datetime(2020, 3, 31),
 dt.datetime(2020, 6, 30)]
#sections

# mask to remove dates when financials are updated
mask = (cleanData['Date'] != dt.datetime(2019, 9, 30)) \
& (cleanData['Date'] != dt.datetime(2019, 12, 31)) \
& (cleanData['Date'] != dt.datetime(2020, 3, 31)) \
& (cleanData['Date'] != dt.datetime(2020, 6, 30)) 
#mask

# remove those dates
cleanData = cleanData[mask].copy()
#cleanData

# remove anything that doesnt happen after sep 30, 2019
mask = (cleanData['Date'] > dt.datetime(2019, 9, 30)) 
cleanData = cleanData[mask].copy()
#cleanData

# replacing some columns as such: 30M -> 30000000, 1.5T -> 1500000000000, 34.2B -> 34200000000
valLookup = {}
valLookup['k'] = 1000
valLookup['M'] = 1000000
valLookup['B'] = 1000000000
valLookup['T'] = 1000000000000
valLookup

def getVal(x):
    try:
        theLetter = re.findall(r'[a-zA-Z]+', x)[0]
        theNumber = re.match(r'(\-*[0-9]*\.[0-9]*)|(\-*[0-9]+)', x)[0]
        x = np.float64(theNumber) * valLookup[theLetter]
        return x
    except:
        try:
            return np.float64(x)
        except:
            return x
    
cleanData = cleanData.applymap(getVal)

# save clean data file
cleanData.to_pickle(cleanDataName2)

# # use this only to get ad-hoc statistics for a particular component
# curSym = 'OXY'
# curUrl = "https://finance.yahoo.com/quote/" + curSym + "/key-statistics?p=" + curSym
# response = requests.get(curUrl)
# if (allSymbols.index(curSym)+1) % 10 == 0:
#     print("working {} out of {}".format(allSymbols.index(curSym)+1, len(allSymbols)))
# soup = BeautifulSoup(response.text,"html.parser")
# table = soup.find('table')
# tr = table.findAll(['tr'])
# csvFile = open("./data/" + curSym + "-Stats.csv",'wt',newline='', encoding='utf-8')
# writer = csv.writer(csvFile)  
# try:   
#         for cell in tr:
#             th = cell.find_all('th')
#             th_data = [col.text.strip('\n') for col in th]
#             td = cell.find_all('td')
#             row = [i.text.replace('\n','') for i in td]
#             writer.writerow(th_data+row)      
# finally:   
#     csvFile.close()
