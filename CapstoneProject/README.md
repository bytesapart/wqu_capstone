## README

1. This program was created using Anaconda2 v4.4.0. However, this should
work on any standard installations of python 2.7.x+
2. To install the packages required to run the program, please find the
requirements.txt file. This file contains all the packages used by the
program. To install, do the following:

    **pip install -r requirements.txt**

3. We also need to install talib. The most reliable way to do so
is via conda using the compiled version distributed by Quantopian.
In order to do that, we need to have conda first on our machine. To install conda,
follow the instructions at [conda docs](https://conda.io/docs/user-guide/install/windows.html). If you
already have Anaconda installed, please execute the following line:

    **conda install -c quantopian ta-lib**
4. The program was developed on Windows 10. The code tends to be
cross-platform, however this has not been tested on a Windows or Mac
machine.

5. The program is launched by typing the following on the command line
(Note: Because of Yahoo finance, sometimes we get no data upon execution and this
will result into the script error-ing out. Please rerun the script if that occurs):

   **python main.py**

6. The script initially asks for tickers to construct a portfolio from.
This could be supplied in an excel file, or typed on the command prompt.

7. Historical EoD data for upto 1 year is fetched from Yahoo Finance

8. Volatility and daily measure are calculated. Stocks are discarded from
the process if they are an outlier with the above critera

9. Measures such as ADX, SMA , Bollinger Bands etc are calculated. 