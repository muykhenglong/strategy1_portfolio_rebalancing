# Portfolio Rebalancing Strategy Backtester

This Python script is designed for backtesting a dynamic portfolio rebalancing strategy using historical data of the Dow Jones Industrial Average components from five years ago. It leverages the Yahoo Finance API (via `yfinance`) to fetch historical stock data, computes monthly returns, and applies a systematic rebalancing strategy to maintain optimal portfolio performance.

## Features

- **Automated Data Fetching**: Retrieves historical stock prices for Dow Jones components.
- **Historical Data Analysis**: Utilizes historical data to simulate the performance of portfolio rebalancing strategies.
- **Dynamic Portfolio Rebalancing**: Implements monthly rebalancing by substituting underperforming stocks with the better-performing ones not currently in the portfolio.
- **Performance Metrics**: Computes key performance indicators (KPIs) such as Compound Annual Growth Rate (CAGR), volatility, Sharpe ratio, and maximum drawdown.

## Requirements

- Python 3.8.19
- yfinance

Ensure you have the necessary Python packages installed: ```pip install yfinance```

## Strategy Description

The rebalancing function pflio evaluates the portfolio every month. It removes a specified number (x) of the worst-performing stocks and adds the same number of top-performing stocks from outside the existing portfolio, aiming to maintain a constant portfolio size (m).

Parameters:
DF: Dataframe containing monthly returns for each stock.
m: Desired number of stocks in the portfolio.
x: Number of underperforming stocks to remove from the portfolio each month.

## How It Works

Data Fetching: Downloads five years of monthly stock data for each Dow component.
Return Calculation: Calculates monthly returns for each stock.
Portfolio Strategy Execution: Applies the rebalancing strategy and calculates various financial metrics to assess performance.
KPI Calculation: Determines CAGR, Sharpe ratio, and maximum drawdown for the rebalanced portfolio as well as for a simple buy-and-hold strategy.

## Author

Muykheng Long - https://github.com/muykhenglong/
