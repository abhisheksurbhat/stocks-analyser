import pandas as pd

def backtest_function(strategy='EMA'):
    '''
        Backtest stock data with indicators. 
        EMA = Exponential Moving Average.
        EOM = Ease of Movement.
        RSI = Relative Strength Index.
    '''
    listOfStocksFile = pd.read_csv('ind_nifty100list.csv')
    symbol_list = listOfStocksFile['Symbol']

    avg_gain_arr = []
    avg_loss_arr = []
    batting_avg_arr = []
    ratio_arr = []
    max_gain_arr = []
    max_loss_arr = []
    totalR_arr = []

    print(f'Backtesting stock data with {strategy} as strategy.')

    for symbol in symbol_list:

        print(f'Backtesting {symbol} stocks..')

        df = pd.read_csv(f'stocks_indicators/{symbol}.NS.csv')

        pos = 0
        percent_change = []

        for i in df.index:
            
            if strategy=='EMA':
                cmin = min(df['EMA_3'][i], df['EMA_5'][i], df['EMA_8'][i], 
                    df['EMA_10'][i], df['EMA_12'][i], df['EMA_15'][i])
                cmax = max(df['EMA_30'][i], df['EMA_35'][i], df['EMA_40'][i], 
                    df['EMA_45'][i], df['EMA_50'][i], df['EMA_60'][i])
            elif strategy=='RSI':
                rsi = df['RSI'][i]
            elif strategy=='EOM':
                eom = df['Ease of Movement'][i]

            close = df['Adj Close'][i]

            if (strategy=='EMA' and cmin>cmax) or (strategy=='RSI' and rsi<30) or (strategy=='EOM' and eom>10):
                if pos == 0:
                    pos = 1
                    bp = close

            elif (strategy=='EMA' and cmin<cmax) or (strategy=='RSI' and rsi>70) or (strategy=='EOM' and eom<-10):
                if pos == 1:
                    pos = 0
                    sp = close
                    pc = (sp/bp -1)*100
                    percent_change.append(pc)
            
            if i == df['Adj Close'].count()-1:
                if pos == 1:
                    pos = 0
                    sp = close
                    pc = (sp/bp -1)*100
                    percent_change.append(pc) 
            
        gains = 0
        losses = 0
        ng = 0
        nl = 0
        totalR = 1

        for i in percent_change:
            if i>0:
                gains += i
                ng += 1
            elif i<0:
                losses += i
                nl += 1
            totalR = totalR*((i/100)+1)

        totalR = round((totalR-1)*100, 2)

        if ng>0:
            avg_gain = gains/ng
            max_gain = max(percent_change)
        else:
            avg_gain = 0
            max_gain = 0

        if nl>0:
            avg_loss = losses/nl
            max_loss = min(percent_change)
            ratio = (-avg_gain/avg_loss)
        else:
            avg_loss = 0
            max_loss = 0
            ratio = -1

        if(ng>0 or nl>0):
            batting_avg=ng/(ng+nl)
        else:
            batting_avg=0

        batting_avg_arr.append(batting_avg)
        ratio_arr.append(ratio)
        avg_gain_arr.append(avg_gain)
        avg_loss_arr.append(avg_loss)
        max_gain_arr.append(max_gain)
        max_loss_arr.append(max_loss)
        totalR_arr.append(totalR)

    print('Backtesting for all stocks done. Printing Results:')

    final_max_gain = max(max_gain_arr)
    final_max_loss = max(max_loss_arr)
    final_batting_avg = sum(batting_avg_arr)/len(batting_avg_arr)
    final_ratio = sum(ratio_arr)/len(ratio_arr)
    final_avg_gain = sum(avg_gain_arr)/len(avg_gain_arr)
    final_avg_loss = sum(avg_loss_arr)/len(avg_loss_arr)
    final_totalR = round(sum(totalR_arr)/len(totalR_arr),2)


    print()
    print(f'Batting Avg: {final_batting_avg}')
    print(f'Gain/loss ratio: {final_ratio}')
    print(f'Average Gain: {final_avg_gain}')
    print(f'Average Loss: {final_avg_loss}')
    print(f'Max Return: {final_max_gain}')
    print(f'Max Loss: {(final_max_loss)}')
    print(f'Total return over all trades: {final_totalR}%') 
    print()