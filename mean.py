import warnings
from database import config
from database import transactionsBT as db
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from scipy import stats

SYMBOL="FB"
TIME_FRAME="History Data (Daily)"
FROM_DATE="01-jun-2019"
TO_DATE="01-Jun-2022"
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
        #  #Reverse index
        # df = df.reindex(index=df.index[::-1])
        # df.reset_index(level=0, inplace=True)
    #    #Rename cols
    #     df = df.rename({
    #     'index': 'dtDate',
    #     '1. Close': 'Close'
    #     },axis=1)
        # df.index= df['dtDate']
        df=df.set_index("dtDate", drop=False, append=False, inplace=False, verify_integrity=False)
        
        #Convert date col to datetime format
        df['dtDate'] = pd.to_datetime(df['dtDate'])
        # df=df.drop(columns=['dtDate'])
        #Short moving averages (5-20 periods) are best suited for short-term trends and trading
        df['mean'] = stats.gmean(df['Close'])
        df['std'] = df['Close'].std()
       
        df['upper_std'] = df['mean'] + (1 * df['std'])
        df['lower_std'] = df['mean'] - (1 * df['std'])
        df['2 upper_std'] = df['mean'] + (2 * df['std'])
        df['2 lower_std'] = df['mean'] - (2 * df['std'])
        print(df)
        #plot for validation
        
        # plt.figure(figsize=(12,5))
        # plt.xticks(rotation=45)

        # plt.plot(df['dtDate'], df['Close'], label = 'Close')
        # plt.plot(df['dtDate'], df['mean'], label = 'mean')
        #plot for validation
        plt.figure(figsize=(12,5))
        plt.xticks(rotation=45)

        x_axis = df['dtDate']

        plt.plot(x_axis, df['Close'], label = 'Close',color='black')
        plt.plot(df['dtDate'], df['mean'], label = 'mean',color='Red')
        #plt.fill_between(x_axis, df['upper_std'], df['lower_std'], label = 'standard', color='lightgrey')
        plt.plot(x_axis,df['upper_std'], label = 'Std above',color='Green')
        plt.plot(x_axis,df['lower_std'], label = 'Std Below',color='Green')
        plt.plot(x_axis,df['2 upper_std'], label = '2 std above',color='Blue')
        plt.plot(x_axis,df['2 lower_std'], label = '2 std below',color='Blue')
       

        plt.title(f'{SYMBOL} Price Chart', fontweight="bold")
        plt.legend()
        plt.show()
        
    except Exception as e:
        print(e)

if __name__=='__main__':        
    main()
