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
        sqlQuery=f"Select top 5 SymName from tblSymbol where IndexName like '%NASDAQ%'"
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
        #df=df.set_index("dtDate", drop=False, append=False, inplace=False, verify_integrity=False)
        df['dtDate'] = pd.to_datetime(df['dtDate'])
        plt.figure(figsize=(12,5))
        plt.xticks(rotation=45)

        x_axis = df['dtDate']
        #x_axis = df['dtDate']
        # df=pd.DatetimeIndex(pd.to_datetime['dtDate'])
       # Create a 'x' and 'y' column for convenience
        df['y'] = df['Close']     # create a new y-col (optional)
        df['x'] = np.arange(len(df))  # create x-col of continuous integers
        # Drop the rows that contain missing days
        df = df.dropna()

        X=df['x'].values[:, np.newaxis]
        y=df['y'].values[:, np.newaxis]

        # Fit linear regression model using scikit-learn
        lin_reg = LinearRegression()
        lin_reg.fit(X, y)
        
        
        
        # Make predictions w.r.t. 'x' and store it in a column called 'y_pred'
        df['y_pred'] = lin_reg.predict(df['x'].values[:, np.newaxis])
        print(np.std(y))
       
        df['upper_std']=df['y_pred']  + np.std(y)*0.80
        df['lower_std']=df['y_pred'] - np.std(y)*0.80
        df['double_std_above']=df['y_pred']  + np.std(y)*1.60
        df['double_std_below']=df['y_pred'] - np.std(y)*1.60
        #print(df.tail()) 
        
        
        close=df["y"].tail(1).values[0]
        
        r2=df['double_std_above'].tail(1).values[0]
        r1=df['upper_std'].tail(1).values[0]
        mean=df['y_pred'].tail(1).values[0]
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
        
        
        # x=pd.Series(np.intersect1d(pd.Series(df["y"]), pd.Series(df['y_pred'])))
        # print(x.count())
        
        
        
        
        
        
        diff = df['y'] > df['upper_std']
        diff_forward = diff.shift(1)
        crossing = np.where(abs(diff - diff_forward) == 1)[0]
        print(crossing)
        
        
        
        df['difference'] = df.y - df.upper_std
        df['cross'] = np.sign(df.difference.shift(1))!=np.sign(df.difference)
        x=np.sum(df.cross)-1
        print(x)
        probability_upper=x/len(df)
        print(probability_upper)
        
        diff = df['y'] > df['double_std_above']
        diff_forward = diff.shift(1)
        crossing = np.where(abs(diff - diff_forward) == 1)[0]
        print(crossing)
        
        df['difference'] = df.y - df.double_std_above
        df['cross'] = np.sign(df.difference.shift(1))!=np.sign(df.difference)
        x=np.sum(df.cross)-1
        print(x)
        probability_upper=x/len(df)
        print(probability_upper)
        
        
        print(df)

        plt.plot(x_axis,df['y'], label = 'Close',color='black')
        plt.plot(df['dtDate'],df['y_pred'], label = 'mean',color='Red')
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
