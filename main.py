import os
import pandas as pd
from helpers.backtest import backtest_function
from helpers.request_stock import fetch_all_data_and_write_to_csv
from helpers.calculate_stock_indices import calculate_ema, calculate_eom, calculate_rsi

# First, check if historic stock data is available. If not, fetch historic 
# stock data and store in CSV files.
if not os.path.isdir('historic_stock_data'):
    os.mkdir('historic_stock_data')
if not os.path.isdir('stocks_indicators'):
    os.mkdir('stocks_indicators')

historic_stock_dir = os.listdir('historic_stock_data')
stock_indicators_dir = os.listdir('stocks_indicators')
if len(historic_stock_dir) == 0:
    start_year = input('Enter starting date to fetch stocks:\n')
    print('Fetching all stocks data...')
    fetch_all_data_and_write_to_csv(int(start_year))

# When historic data is available, iterate over each stock and calculate indicators.

print('Stock data is available. Calculating indicators now...')
csvFile = pd.read_csv('ind_nifty100list.csv')
symbols =  csvFile['Symbol']
for symbol in symbols:
    
    symbol = symbol + '.NS'
    historic_data_file = pd.read_csv(f'historic_stock_data/{symbol}.csv')
    historic_data_file_with_ema = calculate_ema(historic_data_file)
    historic_data_file_with_ema_and_eom = calculate_eom(historic_data_file_with_ema)
    complete_indicators_file = calculate_rsi(historic_data_file_with_ema_and_eom)
    complete_indicators_file = complete_indicators_file.iloc[15:]
    complete_indicators_file = complete_indicators_file.reset_index(drop=True)

    complete_indicators_file.to_csv(f'stocks_indicators/{symbol}.csv', index=False)

print('Indicators are calculated. Would you like to backtest your data against these indicators?(yes/no)')
backtest_data = input()
if backtest_data=='Yes' or backtest_data=='yes' or backtest_data=='y':
    print('The indicators calculated are:')
    print('1. Ease of Movement')
    print('2. Exponential Moving average based crossover')
    print('3. Relative Strength Index')
    print('Please provide the option number to use.')
    backtest_strategy = input('Enter the indicator you would like to use for backtesting:\n')
    if backtest_strategy==1 or backtest_strategy=='1':
        backtest_function(strategy='EOM')
    elif backtest_strategy==2 or backtest_strategy=='2':
        backtest_function(strategy='EMA')
    elif backtest_strategy==3 or backtest_strategy=='3':
        backtest_function(strategy='RSI')
    else:
        print('You have not provided a valid input. Reverting to default strategy')
        backtest_function(strategy='EMA')