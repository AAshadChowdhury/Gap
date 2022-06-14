import warnings
from database import config
from database import transactionsBT as db
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
import numpy as np

SYMBOL="TSLA"
TIME_FRAME="History Data (Daily)"
FROM_DATE="01-Jul-2021"
TO_DATE="01-May-2022"
def main():
    try:
        df=fncGetData()
        fncCheckMean(df)
        # fncCheckMean(fncGetData())
        
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
       
       x = np.arange(df['dtDate'].size)
       fit = np.polyfit(x, df['Close'], deg=1)
       print ("Slope : " + str(fit[0]))
       print ("Intercept : " + str(fit[1]))
       #Fit function : y = mx + c [linear regression ]
       fit_function = np.poly1d(fit)

       #Linear regression plot
       plt.plot(df['dtDate'], fit_function(x))
       #Time series data plot
       plt.plot(df['dtDate'], df['Close'])

       plt.xlabel('dtDate')
       plt.ylabel('Closing Price')
       plt.title('AAPL Close Price')
       plt.show()
       prediction = fit_function(df['dtDate'].size + 14)
       print(prediction)
       print(df) 
        
      
        
    except Exception as e:
        print(e)

if __name__=='__main__':        
    main()
