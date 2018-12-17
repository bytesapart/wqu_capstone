"""
Created on Thu November 08 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10.

Compute KPI
"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import pandas as pd


def Measure_KPI(data, tick, t, l, s, st):
    returns = pd.DataFrame()

    returns['date'] = data['Date']
    returns['ret'] = data['PnL']
    ret = returns.set_index('date')

    KPI = pd.DataFrame()

    cumpnl = ret.cumsum()
    alltime_high = cumpnl.max()
    alltime_low = cumpnl.min()
    wdn = (alltime_high - alltime_low)

    # Max Drawdown
    KPI['Max DWN'] = wdn

    Wins = len(ret[ret > 0].dropna())
    Loss = len(ret[ret < 0].dropna())
    Total = len(ret[ret <> 0].dropna())

    win = str(round(((float(Wins) / float(Total)) * 100), 2)) + '%'
    # Win Percentage
    KPI['Win %'] = win

    l = float(Loss)
    if l:
        win_loss = round((float(Wins) / float(Loss)), 2)
        # Win to Loss Ratio
        KPI['Win-Loss Ratio'] = win_loss
    else:
        # Win to Loss Ratio
        KPI['Win-Loss Ratio'] = 'no loss'
    mean_ret = ((ret[ret <> 0].dropna()).mean()) * 100
    KPI['Mean Ret'] = str(round(mean_ret, 2)) + '%'

    water = (cumpnl.max() - cumpnl).fillna(0).sum()
    earth = (cumpnl - cumpnl.min()).fillna(0).sum()
    KPI['Lake Ratio'] = water / earth

    total_returns = (ret[ret <> 0].dropna()).sum()
    negative_returns = abs(ret[ret < 0]).sum()
    if l:
        # Gain to Pain Ratio
        KPI['Gain-to-Pain Ratio'] = total_returns / negative_returns
    else:
        # Gain to Pain Ratio
        KPI['Gain-to-Pain Ratio'] = 'no loss'

    import datetime
    x = [datetime.datetime.date(i) for i in returns['date']]
    returns['dt'] = x
    days = len(returns.groupby('dt').size())
    FV_PV = data['Close'][days - 1] / data['Close'][0]
    no_of_years = float(days) / 252.00
    cagr = ((FV_PV) ** (1 / no_of_years)) - 1
    # Compounded Annual Growth Rate
    KPI['CAGR'] = cagr

    # Other Factors
    KPI['No of Trades'] = t
    KPI['Long Positions'] = l
    KPI['Short Positions'] = s
    KPI['Stop Losses'] = st

    KPI = KPI.transpose()
    KPI = KPI.rename(columns={"ret": tick.upper()})

    return KPI