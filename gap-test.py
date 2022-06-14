import warnings
from database import config
from database import transactionsBT as db
import pandas as pd
import datetime
import mplfinance as mpf
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import alpaca_trade_api as tradeapi



def main():
    fncGetData()

def fncGetData():
    print(f'Executing function - fncGetData')
    api=tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)
    try:
        SYMBOLS=['TWTR']
        today = datetime.date(2022, 4, 29)
        yesterday = datetime.date(2022, 1, 1)
        bars = api.get_bars(SYMBOLS, TimeFrame.Day, yesterday.isoformat(), today.isoformat()).df
        # print(bars)
        
        #Gap-Up
        bars['previous_high'] = bars['high'].shift(1)
        bars['high_gap'] =bars['low']-bars['previous_high']
        bars['high_gap_per'] =bars['low']/bars['previous_high']
        # print(bars['high_gap']>0)
        hg = bars[(bars.high_gap_per>1.03)]
        print(hg)
        #Gap-down
        # filtered = bars[bars.index.strftime('%Y-%m-%d') == today.isoformat()].copy()
        bars['previous_low'] = bars['low'].shift(1)
        bars['down_gap'] =bars['previous_low']-bars['high']
        bars['down_gap_per'] =bars['previous_low']/bars['high']
        # print(bars['high_gap']>0)
        dg = bars[(bars.down_gap_per>1.02)]
        print(dg)
       
        return
        bars = api.get_bars('TWTR', TimeFrame.Day, '2022-01-01', '2022-04-05').df
        mpf.plot(bars, type='pnf')
        mpf.plot(bars, type='candle', mav=20)
        print(mpf.plot(bars))
        # df.set_index('date', inplace=True)
        
        # print(df)
        return bars
    except Exception as e:
        print(e)
        

def fncDatewise():
    print(f'Executing function - datewise')
    try:
        TICKER='TWTR'
        sqlQuery = f"select * from tblHistoryData where SymName='TWTR' and TimeFrame='History Data (Daily)'"
        df = db.fncGetDataAsPanda(sqlQuery)
        df1=df["Close"].plot(title=f"{TICKER}'s stock price");
        # print(df1)
        return df
    except Exception as e:
        print(e)


if __name__=='__main__':        
    main()
