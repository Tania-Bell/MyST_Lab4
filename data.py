import functions as fn
import pandas as pd
import asyncio

if __name__ == "__main__":
    exchanges = ["binance", "bitfinex", "kraken"]
    run_time = 3  # seconds
    symbol1 = "BTC/USDT"
    symbol2 = "ETH/USDT"
    symbol3 = "ADA/USDT"

    data1 = asyncio.run(fn.multi_orderbooks(exchanges, run_time=run_time, symbol=symbol1))
    data1 = [item for sublist in data1 for item in sublist]
    data1 = pd.DataFrame(data1)

    data2 = asyncio.run(fn.multi_orderbooks(exchanges, run_time=run_time, symbol=symbol2))
    data2 = [item for sublist in data2 for item in sublist]
    data2 = pd.DataFrame(data2)

    data3 = asyncio.run(fn.multi_orderbooks(exchanges, run_time=run_time, symbol=symbol3))
    data3 = [item for sublist in data3 for item in sublist]
    data3 = pd.DataFrame(data3)

data = pd.concat([data1, data2, data3], ignore_index=True)

data.to_csv('files/dat.csv')

data = pd.read_csv('files/dat.csv')

df = fn.dataframe(data)

df.to_csv('files/data_volumes.csv')

df_eff_spread = fn.eff_spread(data)

print(df,df_eff_spread)