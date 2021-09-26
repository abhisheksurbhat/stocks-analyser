import pandas as pd

def calculate_eom(df):
    '''
        Returns a pd.DataFrame with Ease of Movement Indicator calculated for
        the data.
    '''
    box_ratio = 0
    distance = 0
    ease_of_movement = [0]
    x = 1000000

    for index in df.index:
        high = df['High']
        low = df['Low']
        if index > 0:
            distance = (high[index]+low[index]-high[index-1]-low[index-1])/2
            box_ratio = (df['Volume'][index]/x)/(high[index]-low[index])
            ease_of_movement.append(round(distance/box_ratio, 2))
            
    df['Ease of Movement'] = ease_of_movement
    
    return df
        
def calculate_ema(df):
    '''
        Returns a pd.DataFrame with 6 short-term and 6 long-term EMAs calculated. 
    '''
    emasToCalculate = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]
    for x in emasToCalculate:
        ema = x
        df['EMA_'+str(ema)] = round(df['Adj Close'].ewm(span=ema, adjust=False).mean(), 2)

    return df

def calculate_rsi(df, periods=14, ema=True):
    '''
        Returns a pd.DataFrame with the relative strength index.
    '''
    close_delta = df['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    df['RSI'] = rsi
    return df
