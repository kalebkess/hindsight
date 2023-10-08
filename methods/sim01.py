from datetime import datetime, timedelta
import itertools
import os
from typing import List

from dotenv import load_dotenv
import numpy as np
import pandas as pd
import yfinance as yf

load_dotenv()

def download_prices(INDEX:str, symbols:List, start:str = "", end:str = ""):
    """
    download prices for stocks in index
    store in data folder
    """
    # define environment variables
    ROOT_PATH = os.environ.get("ROOT_PATH")

    # define path for universe prices folder
    prices_folder = f"{ROOT_PATH}/data/indices/{INDEX}/prices"

    # download prices and store locally in flat file
    if not os.path.exists(prices_folder):
        os.makedirs(prices_folder)

    for symbol in symbols:
        print(f"downloading prices for {symbol}")
        data = yf.download(symbol, start=start, end=end)
        data.to_csv(f"{prices_folder}/{symbol}.csv")



def simulate(symbols: List):
    """
    calculate returns for all stock combinations
    assuming buy and hold each combination
    """
    # define environment variables
    ROOT_PATH = os.environ.get("ROOT_PATH")

    # define path for universe prices folder
    prices_folder = f"{ROOT_PATH}/data/indices/{INDEX}/prices"

    prices = dict()

    for symbol in symbols:
        data = pd.read_csv(f"{prices_folder}/{symbol}.csv")["Adj Close"].values

        # store prices for each stock in memory
        prices[symbol] = data

    for i in range(len(symbols)):

        r = i + 1
        print(f"r = {r}")

        for combo in itertools.combinations(symbols, r):
             
            print(f"Combination: {combo}")

            # weight of each stock in combination 
            wt = 1.0 / r

            # calculate return assuming buy and hold combination
            
            ret = sum( [prices[symbol][-1] / prices[symbol][0] * wt for symbol in combo]  )

            print(f"ret: {ret}")



if __name__ == "__main__":
    # define universe name
    INDEX = "FAANG"

    # define symbols in universe
    symbols = ["META", "AMZN", "AAPL", "NFLX", "GOOGL"]

    # define time period for backtest (last 30 days)
    start = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    end = datetime.today().strftime("%Y-%m-%d")
    download_prices(INDEX=INDEX, symbols=symbols, start=start, end=end)
    simulate(symbols)

