import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt

yf.pdr_override()

def fetch_all_data_and_write_to_csv(start_year=2015, start_month=1, start_day=1):
    '''
        Fetches all NIFTY100 stock data from the last 20 years, and writes each stock data into a CSV.
    '''
    
    list_of_stocks_file = pd.read_csv('ind_nifty100list.csv')
    symbolList = list_of_stocks_file['Symbol']

    for symbol in symbolList:
        stock = symbol+'.NS'

        start = dt.datetime(start_year, start_month, start_day)
        now = dt.datetime.now()

        stock_data = pdr.get_data_yahoo(stock, start, end=now)

        df_stock = pd.DataFrame(stock_data)

        df_stock.to_csv(f'historic_stock_data/{stock}.csv', index=False)