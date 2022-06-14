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
from statsmodels.sandbox.regression.predstd import wls_prediction_std



MONTH="3m"
SYMBOL=""
TIME_FRAME="History Data (Daily)"
FROM_DATE="01-Apr-2022"
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
        sqlQuery=f"Select top 1 SymName from tblSymbol where IndexName like '%NASDAQ%'"
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
        # plt.figure(figsize=(12,5))
        # plt.xticks(rotation=45)

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
        
        Xc = sm.add_constant(X)
        res = sm.OLS(y, Xc).fit()
        # fitted_model = linear_regression.fit()
        
        
        print(res.summary())
        fig, ax = plt.subplots()
        ax.plot(x_axis, res.fittedvalues, 'r', label="OLS")
        ax.plot(x_axis, res.fittedvalues+np.std(y), 'g', label="upper")
        
        ax.plot(x_axis, res.fittedvalues-np.std(y), 'g', label="lower")
        ax.plot(x_axis, y, 'b', label="OLS")
        
        ax.legend(loc='best')
        plt.show()
        # plt.scatter(y = linear_regression.fittedvalues, x = df['dtDate'])
        # plt.fitted_model()
        
        
        # # Make predictions w.r.t. 'x' and store it in a column called 'y_pred'
        # df['y_pred'] = lin_reg.predict(df['x'].values[:, np.newaxis])
        # print(np.std(y))
       
        # df['upper_std']=df['y_pred']  + np.std(y)
        # df['lower_std']=df['y_pred'] - np.std(y)
        # df['2 std above']=df['y_pred']  + np.std(y)*2.00
        # df['2 std below']=df['y_pred'] - np.std(y)*2.00
        # #print(df.tail()) 
        
        
        # close=df["y"].tail(1).values[0]
        
        # r2=df['2 std above'].tail(1).values[0]
        # r1=df['upper_std'].tail(1).values[0]
        # mean=df['y_pred'].tail(1).values[0]
        # s1=df['lower_std'].tail(1).values[0]
        # s2=df['2 std below'].tail(1).values[0]
        # lst=[r2,r1,mean,s1,s2]
        
        # def find_nearest(array, value):
        #     array = np.asarray(array)
        #     idx = (np.abs(array - value)).argmin()
        #     return array[idx]
        

        # diff=0
        # nearest=find_nearest(lst,close)
        # if nearest>close:
        #   diff=nearest-close
        #   print(f'Nearest value: {nearest}, Difference with resistence: {diff}, Market is uptrend')
        # else:
        #   diff=close-nearest
        #   print(f'Nearest value: {nearest}, Difference with support: {diff}, Market is downtrend')
        
        
        
        
        
        
        
        
        
        
        # # Plot 'y' and 'y_pred' vs 'DateTimeIndex`
        # #color_dict = {'red zero line': '#FF0000', 'blue one line': '#0000FF'}
        # #df[['y', 'y_pred','above','below','2 std above','2 std below']].plot(color=['RED', 'Green', 'Blue'])
        # #plt.fill_between(df['x'],df['upper_std'], df['lower_std'], label = 'standard', color='lightgrey')
        # plt.plot(x_axis,df['y'], label = 'Close',color='black')
        # plt.plot(df['dtDate'],df['y_pred'], label = 'mean',color='Red')
        # plt.plot(x_axis,df['upper_std'], label = 'Std above',color='Green')
        # plt.plot(x_axis,df['lower_std'], label = 'Std Below',color='Green')
        # plt.plot(x_axis,df['2 std above'], label = '2 std above',color='Blue')
        # plt.plot(x_axis,df['2 std below'], label = '2 std below',color='Blue')
        # plt.title(f'{SYMBOL} Price Chart Date from {FROM_DATE} to {TO_DATE}', fontweight="bold")
        # plt.legend()
        # # plt.show()
        # #print(df)
        # dir1=f"img\{MONTH}"
        # filename=f"{SYMBOL}.png"
        # plt.savefig(os.path.join(dir1,filename))
        # print("Symbol:{SYMBOL} saved.")
        
        
        
        
        
        
        
        
        
        
        
        # Y_pred=(abs((df["y"].tail(1)-df['y_pred'].tail(1))))
        # print(f'Distance from regression {Y_pred}')

        
        
        
        
        # Upper_std=abs((df["y"].tail(1)-df['upper_std'].tail(1)))
        # print(f'Distance from Upper_std standard {Upper_std}')
        
        
        # lower_std=abs((df["y"].tail(1)-df['lower_std'].tail(1)))
        # print(f'Distance from lower_std standard {lower_std}')
        
        
        # lower_std=abs((df["y"]-df['lower_std']))
        
        # lower_std=lower_std.min()
        # print(f"Distance min lower_std standard {lower_std}")
        
        
        # Two_Upper_std=abs((df["y"].tail(1)-df['2 std above'].tail(1)))
        # print(f'Distance from Two_Upper_std {Two_Upper_std}')
        
        
        # Two_Lower_std=abs((df["y"].tail(1)-df['2 std below'].tail(1)))
        # print(f'Distance from Two_Lower_std {Two_Lower_std}')
        
        
        # Two_Lower_std=abs((df["y"]-df['2 std below']))
        
        # print(f'Distance min from Two_Lower_std {Two_Lower_std}')
        # Two_Lower_std=Two_Lower_std.min()
        # print(f'Distance min from Two_Lower_std {Two_Lower_std}')
        
        # # print((df["y_pred"]-df['lower_std']).max())
        # # print((df["y_pred"]-df['lower_std']).max())

        
      
        
    except Exception as e:
        print(e)

if __name__=='__main__':        
    main()
