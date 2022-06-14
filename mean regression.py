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
from sklearn.svm import SVR 



MONTH="3m"
SYMBOL=""
TIME_FRAME="History Data (Daily)"
FROM_DATE="01-may-2022"
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
  
  
def predict_prices(dates, prices, x):
        dates = np.reshape(dates,(len(dates), 1)) # convert to 1xn dimension
        x = np.reshape(x,(len(x), 1))
        
        svr_lin  = SVR(kernel='linear', C=1e3)
        svr_poly = SVR(kernel='poly', C=1e3, degree=2)
        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        
        # Fit regression model
        svr_lin .fit(dates, prices)
        svr_poly.fit(dates, prices)
        svr_rbf.fit(dates, prices)
        
        plt.scatter(dates, prices, c='k', label='Data')
        plt.plot(dates, svr_lin.predict(dates), c='g', label='Linear model')
        plt.plot(dates, svr_rbf.predict(dates), c='r', label='RBF model')    
        plt.plot(dates, svr_poly.predict(dates), c='b', label='Polynomial model')
        
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Support Vector Regression')
        plt.legend()
        plt.show()
        
        return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]
           
           
                
          
        
def fncCheckMean(df):
    print(f'Executing function - fncCheckMean')
    try:
        def get_data(df):  
            data = df.copy()
            # data['date'] = data['dtDate'].dt.normalize()
            data['date'] = pd.to_datetime(data['dtDate']).astype(str)
            data['date'] = data['date'].str.split('-').str[2]
            data['date'] = pd.to_numeric(data['date'])
            return [ data['date'].tolist(), data['Close'].tolist() ]
        
        
        dates, prices = get_data(df)
        
        print(dates)
        print(prices)
        
        predicted_price = predict_prices(dates, prices, [31])
        print(predicted_price)
        
        
        
        
        
      
        
    except Exception as e:
        print(e)





if __name__=='__main__':        
    main()
