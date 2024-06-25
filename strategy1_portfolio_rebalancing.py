#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 13:07:01 2024

Strategy 1: Portfolio Rebalancing

@author: Muykheng Long
"""

import pandas as pd
import numpy as np
import datetime
import copy
import matplotlib.pyplot as plt
import yfinance as yf

def CAGR(DF):
    df = DF.copy()
    df['cum_return'] = (1+df['mon_return']).cumprod()
    n = len(df)/12
    CAGR = (df['cum_return'].iloc[-1])**(1/n)-1
    return CAGR

def volatility(DF):
    df = DF.copy()
#    df['mon_return'] = df['Adj Close'].pct_change()
    vol = df['mon_return'].std() * np.sqrt(12)
    return vol

def sharpe(DF, rf):
    sharpe = (CAGR(DF) - rf)/volatility(DF)
    return sharpe    

def max_dd(DF):
    df = DF.copy()
    df['cum_return'] = (1+df['mon_return']).cumprod()
    df['cum_rolling_max'] = df['cum_return'].max()
    df['drawdown'] = df['cum_rolling_max'] - df['cum_return']
    return (df['drawdown']/ df['cum_rolling_max']).max()


def pflio(DF,m,x): 
    """
    Portfolio rebalancing: each month, remove specified number of worst-performing stocks in a portfolio and add other good-performing stocks that are not already in the portfolio 
    (Note that performance of stocks in portfolio is not being compared with stocks outside of the portfolio as the addition/removal criteria.
     That is, good performing stocks that remain in the portfolio may have lower return the best performing stocks in the stock universe)
    DF: dataframe with monthly return for all stocks
    m: number of stocks desired in the portfolio
    x: number of underporforming stocks to be removed from portfolio monthly
    """
    
    df = DF.copy()
    portfolio = []
    portfolio_df = pd.DataFrame()
    mon_return = [0]
    for i in range(1,len(df)):
        if len(portfolio)>0:
            mon_return.append(df[portfolio].iloc[i,:].mean())
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]     
        fill = m-len(portfolio)
        new_picks = df[[t for t in tickers if t not in portfolio]].iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
#        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist() # if want to include existing stock twice
        portfolio = portfolio + new_picks
        portfolio_df[i] = portfolio
        print(portfolio)
    monthly_return_df = pd.DataFrame(np.array(mon_return),columns=['mon_return'])
    return monthly_return_df, portfolio_df
    

# Dow Jones Industrial Average's components as of April 2, 2019
# https://en.wikipedia.org/wiki/Historical_components_of_the_Dow_Jones_Industrial_Average
tickers = ['MMM','AXP','AAPL','BA','CAT','CVX','CSCO','KO','DOW','XOM','GS',
           'HD','INTC','IBM','JNJ','JPM','MCD','MRK','MSFT','NKE',
           'PFE','PG','TRV','UNH','RTX','VZ','V','WBA','WMT','DIS'] # UTX was merged with RTX in 2020: https://www.rtx.com/news/2020/04/03/united-technologies-and-raytheon-complete-merger-of-equals-transaction#:~:text=Upon%20closing%20of%20the%20merger,Technologies%20common%20stock%2C%20which%20now

ohlc_mon = {}

for ticker in tickers: 
    temp = yf.download(ticker,period='5y',interval='1mo')
    temp.dropna(how='any',inplace=True)
    ohlc_mon[ticker] = temp

# Create a dataframe storing monthly return for each stock
ohlc_dic = copy.deepcopy(ohlc_mon)
return_df = pd.DataFrame()
for ticker in tickers:
    print(f'calculating monthly return for {ticker}')
    ohlc_dic[ticker]['mon_return'] = ohlc_dic[ticker]['Adj Close'].pct_change()
    return_df[ticker] = ohlc_dic[ticker]['mon_return']

# Calculate KPIs for the strategy
CAGR(pflio(return_df,6,3))
sharpe(pflio(return_df,6,3), 0.025)
max_dd(pflio(return_df,6,3))

# Calculate KPIs for simple buy and hold
DJI = yf.download('^DJI',period='5y',interval='1mo')
DJI['mon_return'] = DJI['Adj Close'].pct_change()
CAGR(DJI)
sharpe(DJI, 0.025)
max_dd(DJI)
