"""
Created on Thu November 08 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10.

"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import trading_strategy
import measure_kpi
import pandas as pd
import talib


def trading_strat_mean_revert(stock_data):
    # Index data variable
    index_close = stock_data['^GSPC'].Close.values
    index_ma = talib.SMA(stock_data['^GSPC'].Close.values, 40)
    # Bollinger bands Broad Market
    bands_i = talib.BBANDS(stock_data['^GSPC'].Close.values, 40, 1.75, 1.75)
    index_bh = bands_i[0]
    index_bm = bands_i[1]
    index_bl = bands_i[2]
    # ADX of Broad Market
    index_adx = talib.ADX(stock_data['^GSPC'].High.values, \
                          stock_data['^GSPC'].Low.values, \
                          stock_data['^GSPC'].Close.values, 10)
    x = pd.DataFrame()
    y = pd.DataFrame()
    z = any
    KPI = pd.DataFrame()
    # use equal weight portfolio
    investment = 100000
    portfolio_size = len(stock_data) - 1
    investment_each = investment / portfolio_size

    # Loop at the stocks:
    for tick, r in stock_data.iteritems():
        f = pd.DataFrame(r)
        if tick == '^GSPC':
            continue
        else:
            # Index Close
            f['Broad_Close'] = index_close

            # SMA of INDEX
            f['Broad_SMA'] = index_ma

            # Index ADX
            f['Index ADX'] = index_adx

            # Bollinger bands of Index
            f['Index UPBAND'] = index_bh
            f['Index MIDBAND'] = index_bm
            f['Index LOWBAND'] = index_bl

            # Bollinger bands
            bands = talib.BBANDS(r.Close.values, 40, 1.75, 1.75)
            f['UPBAND'] = bands[0]
            f['MIDBAND'] = bands[1]
            f['LOWBAND'] = bands[2]

            # get RSI 
            f['RSI'] = talib.RSI(r.Close.values, 5)

            # DI
            f['PLUS_DI'] = talib.PLUS_DI(r.High.values, r.Low.values, r.Close.values, 10)
            f['MINUS_DI'] = talib.MINUS_DI(r.High.values, r.Low.values, r.Close.values, 10)

            # get ADX 
            f['ADX'] = talib.ADX(r.High.values, r.Low.values, r.Close.values, 10)

            # get MACD 
            f['MACD'], f['SIGNAL'], f['HIST'] = talib.MACD(r.Close.values, 12, 26, 9)

            # get Stochastic
            f['SLOWK'], f['SLOWD'] = talib.STOCH(r.High.values, r.Low.values, r.Close.values, 14, 3, 0, 3, 0)

            # Device strategy
            M, no_of_trades, no_of_long, no_of_short, no_of_stop \
                = trading_strategy.derive_strategy(f, investment_each)

            # compute KPI
            if no_of_trades:
                kpi = measure_kpi.Measure_KPI(M, tick, no_of_trades, no_of_long, no_of_short, no_of_stop)
                KPI = pd.concat([KPI, kpi], axis=1)
            else:
                'No Trades Executed'
            x = (f.reset_index()).copy()
            y = r.copy()
            z = tick

        print KPI
        return x, y, z
