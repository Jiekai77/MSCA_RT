#!/bin/python3

import math
import os
import random
import re
import sys
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


#
# Complete the 'case1' function below.
#
# The function accepts STRING_ARRAY fp_data as parameter.
#

def case1(financial_data):
    print(financial_data.iloc[:5,])
    print(financial_data.iloc[-5:,])
    print(financial_data.describe())
    # Print First 5 rows of MSFT
    # Print Last 5 rows of MSFT
    # Print Describe MSFT

def case2(financial_data):
    re = financial_data.resample('M').mean()
    print(re.iloc[:5,])
    #Resample to monthly data
    #Display the first 5 rows

def case3(financial_data):
    daily_close = pd.DataFrame()
    daily_close['Adj Close'] = (financial_data['Adj Close'].shift(-1)- financial_data['Adj Close'])/financial_data['Adj Close']
    daily_close = daily_close[:-1]
    daily_close.index=financial_data.index[1:]
    print(daily_close)
    # Create a variable daily_close and copy Adj Close from financial_data
    # Print daily returns


def case4(financial_data):
    daily_close = pd.DataFrame()
    daily_close['Adj Close'] = (financial_data['Adj Close'].shift(-1)- financial_data['Adj Close'])/financial_data['Adj Close']
    daily_close = daily_close[:-1]
    daily_close.index=financial_data.index[1:]
    daily_close['Adj Close'][0] += 1
    for i in range(1,len(daily_close['Adj Close'])):
        daily_close['Adj Close'][i] = daily_close['Adj Close'][i-1] * (daily_close['Adj Close'][i]+1)     
    print(daily_close)
    # Calculate the cumulative daily returns
    # Print it

def case5(financial_data):
    daily_close = pd.DataFrame()
    daily_close['Adj Close'] = (financial_data['Adj Close'].shift(-1)- financial_data['Adj Close'])/financial_data['Adj Close']
    daily_close = daily_close[:-1]
    daily_close.index=financial_data.index[1:]
    daily_close['Adj Close'][0] += 1
    for i in range(1,len(daily_close['Adj Close'])):
        daily_close['Adj Close'][i] = daily_close['Adj Close'][i-1] * (daily_close['Adj Close'][i]+1) 
    re = daily_close.resample('M').mean()
    print(re)
    # Resample the cumulative daily return to cumulative monthly return

def case6(financial_data):
    am_20 = pd.DataFrame()
    am_20['Adj Close'] = financial_data['Adj Close'].rolling(window = 20).mean()
    print(am_20)

    # Isolate the adjusted closing prices and store it in a variable
    # Calculate the moving average for a window of 20
    # Display the last 20 moving average number


def case7(financial_data):
    am_100 = pd.DataFrame()
    am_100['Adj Close'] = financial_data['Adj Close'].pct_change().rolling(window = 100).std()*10
    print(am_100)
    # Calculate the volatility for a period of 100 don't forget to multiply by square root
    # don't forget that you need to use pct_change


def case8(financial_data):
    
    
    # Initialize the short rolling window (window=50)
    short_window = 50
    # Initialize the long rolling window (window=100)
    long_window = 100

    # You will create a signals dataframe
    # using the index of financial_data
    signals = pd.DataFrame(index = financial_data.index)
    
    # You will assign 0 to the column signal of the dataframe signals
    signals['signal'] = 0
    # Create short simple moving average over the short window
    signals['short_mavg'] = financial_data['Close'].rolling(window = short_window,min_periods = 1,center = False).mean()
    # Create long simple moving average over the long window
    signals['long_mavg'] = financial_data['Close'].rolling(window = long_window,min_periods = 1,center = False).mean()
    # You will not populate the value 1 when the small window moving average
    # is higher than the long window moving average else 0
    signals['signal']= np.where(signals['short_mavg']>signals['long_mavg'],1.0,0.0)

    # Generate trading orders by inserting in a new column orders
    # 1 if it is a buy order -1 if it is a sell order
    # you should just use the diff command on the column signal
    signals['orders'] = signals['signal'].diff()
    # Print the dataframe signals
    print(signals)
    


def case9(financial_data):
    
    # You will need to use the dataframe signals
    signals = pd.DataFrame(index = financial_data.index)
    signals['signal'] = 0
    signals['short_mavg'] = financial_data['Close'].rolling(window = 50,min_periods = 1,center = False).mean()
    signals['long_mavg'] = financial_data['Close'].rolling(window = 100,min_periods = 1,center = False).mean()
    signals['signal']= np.where(signals['short_mavg']>signals['long_mavg'],1.0,0.0)
    signals['orders'] = signals['signal'].diff()
   

    # You are going to set your initial amount of money you want
    # to invest --- here it is 10,000
    initial = float(10000.0)
    
    # You are going to create a new dataframe positions
    # Remember the index is still the same as signals
    positions = pd.DataFrame(index = signals.index).fillna(0.0)
    
    # You are going to buy 10 shares of MSFT when signal is 1
    # You are going to sell 10 shares of MSFT when signal is -1
    # You will assign these values to the column MSFT of the
    # dataframe positions
    positions['MSFT'] = 10 * signals['signal']
    # You are now going to calculate the notional (quantity x price)
    # for your portfolio. You will multiply Adj Close from
    # the dataframe containing prices and the positions (10 shares)
    # You will store it into the variable portfolio
    portfolio = pd.DataFrame(index = positions.index)
    portfolio['MSFT'] = positions.multiply(financial_data['Adj Close'],axis = 0)
    
    
    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(financial_data['Adj Close'],axis = 0)).sum(axis = 1)
    
    # You will store positions.diff into pos_diff
    pos_diff = positions.diff()
    # You will now add a column cash in your dataframe portfolio
    # which will calculate the amount of cash you have
    # initial_capital - (the notional you use for your different buy/sell)
    portfolio['cash'] = initial - (pos_diff.multiply(financial_data['Adj Close'],axis = 0).sum(axis = 1).cumsum())
    portfolio['total'] = portfolio['cash']+portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    
    # You will now add a column total to your portfolio calculating the part of holding
    # and the part of cash

    # Add `returns` to portfolio

    # Print the first lines of `portfolio`
    print(portfolio)

    

if __name__ == '__main__':
    case_number=input().strip()
    df = pd.read_csv(sys.stdin, header=0, index_col='Date', parse_dates=True)
    globals()['case'+case_number](df)
