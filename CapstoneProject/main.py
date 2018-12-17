"""
Created on Thu November 08 11:02:10 2017+5:30

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10.

Short-Term Trading Strategy based on Volatility and Technical Indicators

1. Get ticker/s from user as an entry, or from a file source. Only stocks are permitted to be used. (Scope change, only allow the user to enter tickers rather than custom data, as much exception handling is required in terms of erroneous data)
2. Generate a portfolio based on the tickers that have been entered, and gather the data (EoD) from a source
3. Plot the outlier stocks based on volatility
4. Generate a signal filter based on SMA, ADX, RSI, BB, MACD
5. Devise a strategy using ADX-MACH-RSI-BB
6. Calculate and plot Key Performance Indicators such as Drawdown, Win-to-Loss Ratio, Gain-to-Pain Ratio and other factors such as Number of trades etc.

"""
# Some Metadata about the script
__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import logging  # Logging class for logging in the case of an error, makes debugging easier
import sys  # For gracefully notifying whether the script has ended or not
import stock_entry  # For getting the ticker list from the user
import data_fetcher  # For fetching data from the web
import volatility_estimator  # For getting the volatility of the outliers
import trading_signals  # For generating signals to trade upon
import indicator_plotting


def main():
    """
    This function is called from the main block. The purpose of this function is to contain all the calls to
    business logic functions
    :return: int - Return 0 or 1, which is used as the exist code, depending on successful or erroneous flow
    """
    # Wrap in a try block so that we catch any exceptions thrown by other functions and return a 1 for graceful exit
    try:
        # ===== Step 1: Get Stock list =====
        tickers = stock_entry.prompt_for_stock_entry()

        # ===== Step 2: Get stock historical data =====
        data = data_fetcher.fetch_stock_hist_data(tickers)

        # ===== Step 3: Get the volatility of the outliers =====
        volatility, data = volatility_estimator.calculate_volatility_of_stocks(data)

        # ===== Step 4: Get the indicators to trade on ======
        indicators, data, tick = trading_signals.trading_strat_mean_revert(data)

        # Plot the stock data and the indicators
        indicator_plotting.plot_signals_and_indicators(tick, data, indicators)

    except BaseException, e:
        # Casting a wide net to catch all exceptions
        print('\n%s' % str(e))
        return 1


# Main block of the program. The program begins execution from this block when called from a cmd
if __name__ == '__main__':
    # Initialize Logger
    logging.basicConfig(format='%(asctime)s %(message)s: ')
    logging.info('Application Started')
    exit_code = main()
    logging.info('Application Ended')
    sys.exit(exit_code)
