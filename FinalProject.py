
# Importing necessary libraries
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.cryptocurrencies import CryptoCurrencies

import requests
import pandas as pd

api_key = "36CEU40I8F02M7SS"
outputsize = 'compact'

# Following code gets the list of Symbols i.e ticker for Stocks of S&P 500 Companies
# To facilitate the user to choose the listed company's stock for Data Analysis
pd.set_option('display.max_rows', None)
data = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
tickers = data[0]
tickers = tickers.loc[:,['Symbol', 'Security']]
print("Displaying the list of symbols for stocks of S&P 500")
print("-----------------------------------------------------")
print(tickers)

while True:
# 1. TIME SERIES STOCK DATA
# Time Series Stock API INTRADAY returns Intraday time series of the equity specified.
# This API returns most recent 1-2 months intraday data(used for trading strategy development)
# Ask user to input Ticker i.e Symbol for the company the user wants to analyse the data of
    choice = input("TimeSeries Data, Fundamental Data or Foreign Exchange: ")
    if choice == 'TimeSeries Data':
        ts = TimeSeries(key=api_key, output_format='pandas')
        symbol = input("Enter Ticker for TimeSeries Data: ")
        if symbol == '':
            break
        typ = input("Data type for Time series of " + str(symbol) + " 'daily', 'weekly', 'monthly', 'interval': ")
        if typ == 'daily':
            time_data = ts.get_daily_adjusted(symbol, outputsize)
            print("\n")
            print("TimeSeries daily adjusted for " + str(symbol))
        elif typ == 'weekly':
            time_data = ts.get_weekly_adjusted(symbol)
            print("\n")
            print("TimeSeries weekly adjusted for " + str(symbol))
        elif typ == 'monthly':
            time_data = ts.get_monthly_adjusted(symbol)
            print("\n")
            print("TimeSeries monthly adjusted for " + str(symbol))
        elif typ == 'interval':
            interval = input("Interval :- 1min, 5min, 10min, 15min, 30min, 60min: ")
            time_data = ts.get_intraday(symbol, interval = interval, outputsize = 'compact')
            print("\n")
            print("TimeSeries intraday interval for " + str(symbol))
        print(time_data)

# Fundamental Data covers key financial metrics,income statement, balance sheet and company overview
    elif choice == 'Fundamental Data':
        fd = FundamentalData(key='api_key', output_format='pandas')
        symbol = input("Enter Ticker for Fundamental Data: ")
        if symbol == '':
            break
        period = input("annual or quarterly: ")
        stmt = input("Statement - balance sheet, income statement or cash flow: ")

        if period == 'annual':
            if stmt == 'balance sheet':
                stmt_data = fd.get_balance_sheet_annual(symbol)[0].T[2:]
                stmt_data.columns = list(fd.get_balance_sheet_annual(symbol)[0].T.iloc[0])
                print("\n")
                print("Annual Balance sheet information of " + str(symbol))
            elif stmt == 'income statement':
                stmt_data = fd.get_income_statement_annual(symbol)[0].T[2:]
                stmt_data.columns = list(fd.get_income_statement_annual(symbol)[0].T.iloc[0])
                print("\n")
                print("Annual Income Statement of " + str(symbol))
            elif stmt == 'cash flow':
                stmt_data = fd.get_cash_flow_annual(symbol)[0].T[2:]
                stmt_data.columns = list(fd.get_cash_flow_annual(symbol)[0].T.iloc[0])
                print("\n")
                print("Annual Cash Flow information of " + str(symbol))
            else:
                print("wrong entry.")
            print(stmt_data)
        elif period == 'quarterly':
            if stmt == 'balance sheet':
                stmt_data = fd.get_balance_sheet_quarterly(symbol)[0].T[2:]
                stmt_data.columns = list(fd.get_balance_sheet_quarterly(symbol)[0].T.iloc[0])
                print("\n")
                print("Quarterly Balance sheet information of " + str(symbol))
            elif stmt == 'income statement':
                stmt_data = fd.get_income_statement_quarterly(symbol)[0].T[2:]
                stmt_data.columns = list(fd.get_income_statement_quarterly(symbol)[0].T.iloc[0])
                print("\n")
                print("Quarterly Income Statement information of " + str(symbol))
            elif stmt == 'cash flow':
                stmt_data = fd.get_cash_flow_quarterly(symbol)[0].T[2:]
                stmt_data.columns = list(fd.get_cash_flow_quarterly(symbol)[0].T.iloc[0])
                print("\n")
                print(f"Quarterly Cash Flow information of {symbol}" )
        print(stmt_data)
    elif choice == 'Foreign Exchange':
        user_choice_convert = input("physical currency or crypto currency: ")
        from_curr = input("Your currency: ")
        to_curr = input("Desired currency: ")
        fx = ForeignExchange(api_key, output_format='pandas')
        cc = CryptoCurrencies(api_key, output_format= 'pandas')

        if user_choice_convert == 'physical currency':
            curr_rate = fx.get_currency_exchange_rate(from_curr, to_curr)[0].T.iloc[0:]
        else:
            curr_rate = cc.get_digital_currency_exchange_rate(from_curr,to_curr)[0].T.iloc[0:]
        print(curr_rate)

    elif not choice:
        print("Invalid Entry.")
        break










