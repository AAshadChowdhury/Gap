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
    # datewise()
    
def fncGetData():
    print(f'Executing function - fncGetData')
    api=tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)
    try:
        SYMBOLS=['TWTR']
        #SYMBOLS = ['MMM','AOS','ABT','ABBV','ABMD','ACN','ATVI','ADM','ADBE','ADP','AAP','AES','AFL','A','AIG','APD','AKAM','ALK','ALB','ARE','ALGN','ALLE','LNT','ALL','GOOGL','GOOG','MO','AMZN','AMCR','AMD','AEE','AAL','AEP','AXP','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','APA','AAPL','AMAT','APTV','ANET','AIZ','T','ATO','ADSK','AZO','AVB','AVY','BKR','BLL','BAC','BBWI','BAX','BDX','WRB','BRK.B','BBY','BIO','TECH','BIIB','BLK','BK','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BRO','BF.B','CHRW','CDNS','CZR','CPT','CPB','COF','CAH','KMX','CCL','CARR','CTLT','CAT','CBOE','CBRE','CDW','CE','CNC','CNP','CDAY','CERN','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CI','CINF','CTAS','CSCO','C','CFG','CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','COP','ED','STZ','CEG','COO','CPRT','GLW','CTVA','COST','CTRA','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DXCM','FANG','DLR','DFS','DISH','DIS','DG','DLTR','D','DPZ','DOV','DOW','DTE','DUK','DRE','DD','DXC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ENPH','ETR','EOG','EPAM','EFX','EQIX','EQR','ESS','EL','ETSY','RE','EVRG','ES','EXC','EXPE','EXPD','EXR','XOM','FFIV','FDS','FAST','FRT','FDX','FITB','FRC','FE','FIS','FISV','FLT','FMC','F','FTNT','FTV','FBHS','FOXA','FOX','BEN','FCX','AJG','GRMN','IT','GE','GNRC','GD','GIS','GPC','GILD','GL','GPN','GM','GS','GWW','HAL','HIG','HAS','HCA','PEAK','HSIC','HSY','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HWM','HPQ','HUM','HII','HBAN','IEX','IDXX','ITW','ILMN','INCY','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JBHT','JKHY','J','JNJ','JCI','JPM','JNPR','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KHC','KR','LHX','LH','LRCX','LW','LVS','LDOS','LEN','LLY','LNC','LIN','LYV','LKQ','LMT','L','LOW','LUMN','LYB','MTB','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MTCH','MKC','MCD','MCK','MDT','MRK','FB','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MRNA','MHK','MOH','TAP','MDLZ','MPWR','MNST','MCO','MS','MOS','MSI','MSCI','NDAQ','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NDSN','NSC','NTRS','NOC','NLOK','NCLH','NRG','NUE','NVDA','NVR','NXPI','ORLY','OXY','ODFL','OMC','OKE','ORCL','OGN','OTIS','PCAR','PKG','PARA','PH','PAYX','PAYC','PYPL','PENN','PNR','PEP','PKI','PFE','PM','PSX','PNW','PXD','PNC','POOL','PPG','PPL','PFG','PG','PGR','PLD','PRU','PEG','PTC','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTX','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL','SPGI','CRM','SBAC','SLB','STX','SEE','SRE','NOW','SHW','SBNY','SPG','SWKS','SJM','SNA','SEDG','SO','LUV','SWK','SBUX','STT','STE','SYK','SIVB','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','TDY','TFX','TER','TSLA','TXN','TXT','TMO','TJX','TSCO','TT','TDG','TRV','TRMB','TFC','TWTR','TYL','TSN','USB','UDR','ULTA','UAA','UA','UNP','UAL','UNH','UPS','URI','UHS','VLO','VTR','VRSN','VRSK','VZ','VRTX','VFC','VTRS','V','VNO','VMC','WAB','WMT','WBA','WBD','WM','WAT','WEC','WFC','WELL','WST','WDC','WRK','WY','WHR','WMB','WTW','WYNN','XEL','XYL','YUM','ZBRA','ZBH','ZION','ZTS']
        
        sqlQuery = "With CTE as(Select dtDate, [open], [high], [low], [close], volume, vwap, symName, Case When [close]> Lag([close],1) Over(Partition By SymName order by dtDate) Then Case when [low] - Lag([high],1) Over(Partition By SymName order by dtDate)>0 then [low] - Lag([high],1) Over(Partition By SymName order by dtDate) else 0 end Else Case when Lag([low],1) Over(Partition By SymName order by dtDate)-[high] > 0 then Lag([low],1) Over(Partition By SymName order by dtDate)-[high] else 0 end End 'Gap'from tblHistoryData Where TimeFrame='History Data (Daily)')Select *, [close]*Gap/100.0 Gap_Percent from CTE Where Gap !=0 and [close]*Gap/100.0>3.0 and SymName = 'TWTR' Order By SymName, dtDate"

        today = datetime.date(2022, 5, 5)
        yesterday = datetime.date(2022, 1, 1)
        # df = db.fncGetDataAsPanda(sqlQuery)
        bars = api.get_bars(SYMBOLS, TimeFrame.Day, yesterday.isoformat(), today.isoformat()).df
        # print(bars)
        bars['previous_close'] = bars['close'].shift(1)
        # print(bars)
        filtered = bars[bars.index.strftime('%Y-%m-%d') == today.isoformat()].copy()
        # print(filtered)
        filtered['percent'] = filtered['open'] / filtered['previous_close']
        # print(filtered)
        gap_ups = filtered[filtered['percent'] > 1.03]
        print(gap_ups)
        gap_ups_symbols = gap_ups['symbol'].tolist()
        print(gap_ups_symbols)
        gap_downs = filtered[filtered['percent'] < 0.98]
        print(gap_downs)
        gap_down_symbols = gap_downs['symbol'].tolist()
        print(gap_down_symbols)
        return
    
        # bars = api.get_bars('TWTR', TimeFrame.Day, '2022-01-01', '2022-04-05').df
        print(mpf.plot(bars))
        # df.set_index('date', inplace=True)
        
        # print(df)
        return bars
    except Exception as e:
        print(e)
        

def datewise():
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
   
   
# SYMBOLS = ['MMM','AOS','ABT','ABBV','ABMD','ACN','ATVI','ADM','ADBE','ADP','AAP','AES','AFL','A','AIG','APD','AKAM','ALK','ALB','ARE','ALGN','ALLE','LNT','ALL','GOOGL','GOOG','MO','AMZN','AMCR','AMD','AEE','AAL','AEP','AXP','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','APA','AAPL','AMAT','APTV','ANET','AIZ','T','ATO','ADSK','AZO','AVB','AVY','BKR','BLL','BAC','BBWI','BAX','BDX','WRB','BRK.B','BBY','BIO','TECH','BIIB','BLK','BK','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BRO','BF.B','CHRW','CDNS','CZR','CPT','CPB','COF','CAH','KMX','CCL','CARR','CTLT','CAT','CBOE','CBRE','CDW','CE','CNC','CNP','CDAY','CERN','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CI','CINF','CTAS','CSCO','C','CFG','CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','COP','ED','STZ','CEG','COO','CPRT','GLW','CTVA','COST','CTRA','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DXCM','FANG','DLR','DFS','DISH','DIS','DG','DLTR','D','DPZ','DOV','DOW','DTE','DUK','DRE','DD','DXC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ENPH','ETR','EOG','EPAM','EFX','EQIX','EQR','ESS','EL','ETSY','RE','EVRG','ES','EXC','EXPE','EXPD','EXR','XOM','FFIV','FDS','FAST','FRT','FDX','FITB','FRC','FE','FIS','FISV','FLT','FMC','F','FTNT','FTV','FBHS','FOXA','FOX','BEN','FCX','AJG','GRMN','IT','GE','GNRC','GD','GIS','GPC','GILD','GL','GPN','GM','GS','GWW','HAL','HIG','HAS','HCA','PEAK','HSIC','HSY','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HWM','HPQ','HUM','HII','HBAN','IEX','IDXX','ITW','ILMN','INCY','IR','INTC','ICE','IBM','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JBHT','JKHY','J','JNJ','JCI','JPM','JNPR','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KHC','KR','LHX','LH','LRCX','LW','LVS','LDOS','LEN','LLY','LNC','LIN','LYV','LKQ','LMT','L','LOW','LUMN','LYB','MTB','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MTCH','MKC','MCD','MCK','MDT','MRK','FB','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MRNA','MHK','MOH','TAP','MDLZ','MPWR','MNST','MCO','MS','MOS','MSI','MSCI','NDAQ','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NDSN','NSC','NTRS','NOC','NLOK','NCLH','NRG','NUE','NVDA','NVR','NXPI','ORLY','OXY','ODFL','OMC','OKE','ORCL','OGN','OTIS','PCAR','PKG','PARA','PH','PAYX','PAYC','PYPL','PENN','PNR','PEP','PKI','PFE','PM','PSX','PNW','PXD','PNC','POOL','PPG','PPL','PFG','PG','PGR','PLD','PRU','PEG','PTC','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTX','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL','SPGI','CRM','SBAC','SLB','STX','SEE','SRE','NOW','SHW','SBNY','SPG','SWKS','SJM','SNA','SEDG','SO','LUV','SWK','SBUX','STT','STE','SYK','SIVB','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','TDY','TFX','TER','TSLA','TXN','TXT','TMO','TJX','TSCO','TT','TDG','TRV','TRMB','TFC','TWTR','TYL','TSN','USB','UDR','ULTA','UAA','UA','UNP','UAL','UNH','UPS','URI','UHS','VLO','VTR','VRSN','VRSK','VZ','VRTX','VFC','VTRS','V','VNO','VMC','WAB','WMT','WBA','WBD','WM','WAT','WEC','WFC','WELL','WST','WDC','WRK','WY','WHR','WMB','WTW','WYNN','XEL','XYL','YUM','ZBRA','ZBH','ZION','ZTS']
 
    
# api = rest()

# today = datetime.date(2022, 4, 4)
# yesterday = datetime.date(2022, 4, 1)

# bars = api.get_bars(SYMBOLS, TimeFrame.Day, yesterday.isoformat(), today.isoformat()).df
# print(bars)