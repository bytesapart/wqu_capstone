"""
Created on Thu November 08 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10.

Short-Term Trading Strategy based on Volatility and Technical Indicators

This module fetches data from Yahoo Finance. Please note that since Yahoo
retired their Finance module in 2017, this uses fix_yahoo_finance package
in order to fetch data from Yahoo Finance

"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import warnings  # For removing Deprecation Warning w.r.t. Yahoo Finance Fix
import logging  # For getting all the logs
import datetime  # For getting the datetime
from pandas_datareader import data as pdr  # For fetching the data

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fix_yahoo_finance import pdr_override  # For overriding Pandas DataFrame Reader not connecting to YF


def yahoo_finance_bridge():
    """
    This function fixes problems w.r.t. fetching data from Yahoo Finance
    :return: None
    """
    logging.info('Correcting Yahoo Finance')
    pdr_override()


def fetch_stock_hist_data(stocks):
    """
    This function does the actual heavy-lifting of taking data from Yahoo Finance
    :param stocks: The list of stock tickers whose data needs to be fetched
    :type stocks: diction
    
    :return: dict: A dictionary of DataFrames consisting of data with a time span of a year
    """
    # ===== Step 1: Override Yahoo Finance Bridge =====
    # Fix Pandas Datareader's Issues with Yahoo Finance (Since yahoo abandoned it's API)
    yahoo_finance_bridge()

    # ===== Step 2: Set the appropriate dates =====
    todays_date = datetime.date.today()  # Get Today's date
    end = todays_date
    start = todays_date.replace(year=todays_date.year - 1)  # Fetch the data of past one year
    # Create a dictionary to store all the data
    all_data = {}
    # Initialize iterator variable
    i = 0

    # ===== Step 3: Fetch the appropriate data =====
    for ticker in stocks:
        i += 1
        try:
            # Get data from Yahoo Finance
            all_data[ticker] = pdr.get_data_yahoo(ticker, start, end, auto_adjust=True)
        except IOError:
            continue
    return all_data
