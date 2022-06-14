import warnings
from database import config
from database import transactionsBT as db
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
import numpy as np
import time
import seaborn as sns
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import os
from scipy import stats

MONTH="12m"
SYMBOL=""
TIME_FRAME="History Data (Daily)"
FROM_DATE="01-Jun-2021"
TO_DATE="01-Jun-2022"
def main():
    global SYMBOL
    try:
        Symbols = fncGetSymbols()['SymName']
        for symbol in Symbols:
            SYMBOL=symbol
            
            df=fncGetData()
            fncCheckMean(df)
        # fncCheckMean(fncGetData())
        
    except Exception as e:
        print(e)
        
def fncGetSymbols():
    print(f'Executing function - fncGetSymbols')
    try:
        sqlQuery=f"Select top 3 SymName from tblSymbol where IndexName like '%NASDAQ%'"
        df=db.fncGetDataAsPanda(sqlQuery)
        # print(df[0])
        # print(df)
        return df
    except Exception as e:
        print(e)
              
def fncGetData():
    print(f'Executing function - fncGetData')
    try:
        sqlQuery=f"Select [dtDate],[Close] from tblHistoryData where SymName='{SYMBOL}' and TimeFrame='{TIME_FRAME}' and \
            dtDate between '{FROM_DATE}' and '{TO_DATE}'"
        df=db.fncGetDataAsPanda(sqlQuery)
        # print(df)
        return df
    except Exception as e:
        print(e)
        
def fncCheckMean(df):
    print(f'Executing function - fncCheckMean')
    try:
      
        # df=df.set_index("dtDate", drop=False, append=False, inplace=False, verify_integrity=False)
        
        #Convert date col to datetime format
        df['dtDate'] = pd.to_datetime(df['dtDate'])
        # df=df.drop(columns=['dtDate'])
        #Short moving averages (5-20 periods) are best suited for short-term trends and trading
        df['mean'] = stats.gmean(df['Close'])
        df['std'] = df['Close'].std()
       
        df['upper_std'] = df['mean'] + df['std']
        df['lower_std'] = df['mean'] - df['std']
        df['double_std_above'] = df['mean'] + (df['std']*2)
        df['double_std_below'] = df['mean'] - (df['std']*2)
        # print(df)
    
        plt.figure(figsize=(12,5))
        plt.xticks(rotation=45)

        x_axis = df['dtDate']
        
        
        close=df["Close"].tail(1).values[0]
        
        r2=df['double_std_above'].tail(1).values[0]
        r1=df['upper_std'].tail(1).values[0]
        mean=df['mean'].tail(1).values[0]
        s1=df['lower_std'].tail(1).values[0]
        s2=df['double_std_below'].tail(1).values[0]
        lst=[r2,r1,mean,s1,s2]
        
        def find_nearest(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]
        

        diff=0
        nearest=find_nearest(lst,close)
        if nearest>close:
          diff=nearest-close
          print(f'Nearest value: {nearest}, Difference with resistance: {diff}, Market is uptrend')
        else:
          diff=close-nearest
          print(f'Nearest value: {nearest}, Difference with support: {diff}, Market is downtrend')
        
        
        diff = df['Close'] > df['upper_std']
        diff_forward = diff.shift(1)
        crossing = np.where(abs(diff - diff_forward) == 1)[0]
        print(crossing)
        
        
        
        df['difference'] = df.Close - df.upper_std
        df['cross'] = np.sign(df.difference.shift(1))!=np.sign(df.difference)
        x=np.sum(df.cross)-1
        print(x)
        probability_upper=x/len(df)
        print(probability_upper)
        
        diff = df['Close'] > df['double_std_above']
        diff_forward = diff.shift(1)
        crossing = np.where(abs(diff - diff_forward) == 1)[0]
        print(crossing)
        
        df['difference'] = df.Close - df.double_std_above
        df['cross'] = np.sign(df.difference.shift(1))!=np.sign(df.difference)
        x=np.sum(df.cross)-1
        print(x)
        probability_upper=x/len(df)
        print(probability_upper)
        
        
        print(df)
        
        #  def buy_sell(data):
        #     signalBuy = []
        #     signalSell = []
        #     position = False 

        #     for i in range(len(data)):
        #         if data['SMA 30'][i] > data['SMA 100'][i]:
        #             if position == False :
        #                 signalBuy.append(data['Adj Close'][i])
        #                 signalSell.append(np.nan)
        #                 position = True
        #             else:
        #                 signalBuy.append(np.nan)
        #                 signalSell.append(np.nan)
        #         elif data['SMA 30'][i] < data['SMA 100'][i]:
        #             if position == True:
        #                 signalBuy.append(np.nan)
        #                 signalSell.append(data['Adj Close'][i])
        #                 position = False
        #             else:
        #                 signalBuy.append(np.nan)
        #                 signalSell.append(np.nan)
        #         else:
        #             signalBuy.append(np.nan)
        #             signalSell.append(np.nan)
        #     return pd.Series([signalBuy, signalSell])
        
        
        
        
        
        
       
        plt.plot(x_axis,df['Close'], label = 'Close',color='black')
        plt.plot(x_axis,df['mean'], label = 'mean',color='Red')
        plt.plot(x_axis,df['upper_std'], label = 'Std above',color='Green')
        plt.plot(x_axis,df['lower_std'], label = 'Std Below',color='Green')
        plt.plot(x_axis,df['double_std_above'], label = '2 std above',color='Blue')
        plt.plot(x_axis,df['double_std_below'], label = '2 std below',color='Blue')
        plt.title(f'{SYMBOL} Price Chart Date from {FROM_DATE} to {TO_DATE}', fontweight="bold")
        plt.legend()
        #plt.show()
        #print(df)
        dir1=f"img\{MONTH}"
        filename=f"{SYMBOL}.png"
        plt.savefig(os.path.join(dir1,filename))
        print(f"Symbol:{SYMBOL} saved.")
        
        
    except Exception as e:
        print(e)

if __name__=='__main__':        
    main()
