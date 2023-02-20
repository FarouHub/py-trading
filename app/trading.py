import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

df = pd.read_csv('../datas/BTCUSDT-5m-2023-02-18.csv')

# df['open_time'] = df['open_time'].dt.date
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
# df['open_time'] = datetime.fromtimestamp(math.floor(df['open_time'].str))
# df['open_time'] = pd.to_datetime(df['open_time'], format = '%d.%m.%Y %H:%M:%S')

# print(datetime.fromtimestamp(math.floor(1676678699)))
df.set_index('open_time', inplace=True)

df = df[df.high != df.low]


df['VWAP'] = ta.vwap(df.high, df.low, df.close, df.volume)
df['RSI'] = ta.rsi(df.close, length = 16)
my_bbands = ta.bbands(df.close, length = 14, std = 2.0)
df = df.join(my_bbands)

####
VWAPsignal = [0] * len(df)
backcandles = 15

for row in range(backcandles, len(df)):
    upt = 1
    dnt = 1

    for i in range(row - backcandles, row + 1):
        if max(df.open[i], df.close[i]) >= df.VWAP[i]:
            dnt = 0

        if min(df.open[i], df.close[i]) <= df.VWAP[i]:
            upt = 0
    
    if upt == 1 and dnt == 1:
        VWAPsignal[row] = 3
    elif upt == 1:
        VWAPsignal[row] = 2
    elif dnt == 1:
        VWAPsignal[row] = 1

df['VWAPsignal'] = VWAPsignal

########
def TotalSignal(l):
    if(df.VWAPsignal[l] == 2 and df.close[l] <= df['BBL_14_2.0'][l] and df.RSI[l] < 45):
        return 2
    
    if(df.VWAPsignal[l] == 1 and df.close[l] >= df['BBU_14_2.0'][l] and df.RSI[l] > 55):
        return 1
    
    return 0

TotSignal = [0] * len(df)

for row in range(backcandles, len(df)): # careful backcandles used previous
    TotSignal[row] = TotalSignal(row)

df['TotalSignal'] = TotSignal

df[df.TotalSignal != 0].count()


########
def pointposbreak(x):
    if x['TotalSignal'] == 1:
        return x['high'] + 1e-4
    elif x['TotalSignal'] == 2:
        return x['low'] - 1e-4
    else:
        return np.nan
    
df['pointposbreak'] = df.apply(lambda row: pointposbreak(row), axis = 1)

df.to_csv('../datas/file.csv')
print(df)
########
st = 10400
dfpl = df[st:st+350]
dfpl.reset_index(inplace = True)
fig = go.Figure(data = [go.Candlestick(x = dfpl.index, 
                                       open = dfpl['open'], 
                                       high = dfpl['high'], 
                                       low = dfpl['low'], 
                                       close = dfpl['close']),
                                       go.Scatter(x = dfpl.index, y = dfpl.VWAP, line = dict(color='blue', width = 1), name = 'VWAP'),
                                       go.Scatter(x = dfpl.index, y = dfpl['BBL_14_2.0'], line = dict(color='green', width = 1), name = 'BBL'),
                                       go.Scatter(x = dfpl.index, y = dfpl['BBU_14_2.0'], line = dict(color='green', width = 1), name = 'BBU')
                                    ])
fig.add_scatter(x = dfpl.index, 
                y = dfpl['pointposbreak'],
                mode = 'markers',
                marker = dict(size = 4, color = 'MediumPurple'),
                name = 'Signal')
fig.show()