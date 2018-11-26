"""
Created on Thu November 08 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10.

Short-Term Trading Strategy based on Volatility and Technical Indicators

This module is an "interaction" module that allows the use to enter
the tickers that he wants for his portfolio. This could be in the
form of a file or a ticker list given on the command prompt
The user enters "F" for file, which then accepts a file as a single columnar
csv. The other option is to accept a list of tickers with the help of
the "T" command

"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

# Imports to the file
from builtins import input  # For python 2-3 compatibility
import logging  # Logging class for logging in the case of an error, makes debugging easier
import os  # For os related operations
import pandas as pd  # For loading the csv single columnar file


def prompt_for_stock_entry():
    # print('Please note that the program supports Stocks listed in S&P500 as of now')
    print('This program only accepts tickers that are listed on the SnP500. \nAny other tickers'
          ' may invariable lead to failure in fetching of data, resulting into premature'
          ' exiting of the script. \nPlease make sure to enter only those tickers that are '
          ' available in the SnP500.')
    user_mode = input('Press "F" to load from or a file, or press "T" to input a tickers manually:\n')
    assert isinstance(user_mode, str)  # Assert to make sure that the input provided is a a string
    stock_ticker_array = []

    if user_mode.lower() != 'f' and user_mode.lower() != 't':
        raise ValueError("\nIncorrect entry!\ Please enter only 'F' or 'T'")

    # If the user mode is to fetch from a file
    if user_mode.lower() == 'f':
        user_input = input("Please enter the absolute path to the ticker file. \n"
                           "NOTE 1: Please make sure that the file is a single columnar .xlsx file \n"
                           "NOTE 2: Please make sure that the first row is the header row with name as 'TICKERS': ")
        assert os.path.exists(user_input), "Invalid path provided. Could not find the file at, " + str(user_input)

        # open the file
        excel_file = pd.ExcelFile(user_input)
        ticker_list_from_file = excel_file.parse(0)
        stock_ticker_array = (ticker_list_from_file['TICKERS'].values.tolist())

    # If the user chooses to upload things manually
    else:  # to upload manually
        stock_count = input('Input the number of stocks in the portfolio: \n')
        if stock_count.isdigit():
            stock_count = int(stock_count)
        else:
            raise ValueError('Please enter a number for the number of stocks in a portfolio.')

        for i in range(1, stock_count + 1):
            tickers_from_console = raw_input('Please enter the stock ticker for stock number ' + str(i) + ': \n')
            stock_ticker_array.append(str(tickers_from_console))

    # Broad Market Index is entered
    stock_ticker_array.append('^GSPC')
    return stock_ticker_array


def is_number(var):
    try:
        if var == int(var):
            return True
    except Exception:
        return False