import functions as fn
import pandas as pd
import asyncio

if __name__ == "__main__":
    exchange1 = ["binance"]
    exchange2 = ["bitfinex"]
    exchange3 = ["huobi"]
    run_time = 3600  # seconds
    symbol1 = "BTC/USDT"
    symbol2 = "ETH/USDT"
    symbol3 = "ADA/USDT"  

    data2 = asyncio.run(fn.multi_orderbooks(exchange1, run_time=run_time, symbol=symbol1))
    data2 = [item for sublist in data2 for item in sublist]
    data2 = pd.DataFrame(data2)

    data3 = asyncio.run(fn.multi_orderbooks(exchange1, run_time=run_time, symbol=symbol2))
    data3 = [item for sublist in data3 for item in sublist]
    data3 = pd.DataFrame(data3)

    data5 = asyncio.run(fn.multi_orderbooks(exchange2, run_time=run_time, symbol=symbol1))
    data5 = [item for sublist in data5 for item in sublist]
    data5 = pd.DataFrame(data5)

    data6 = asyncio.run(fn.multi_orderbooks(exchange2, run_time=run_time, symbol=symbol2))
    data6 = [item for sublist in data6 for item in sublist]
    data6 = pd.DataFrame(data6)

    data7 = asyncio.run(fn.multi_orderbooks(exchange3, run_time=run_time, symbol=symbol1))
    data7 = [item for sublist in data7 for item in sublist]
    data7 = pd.DataFrame(data7)

    data8 = asyncio.run(fn.multi_orderbooks(exchange3, run_time=run_time, symbol=symbol2))
    data8 = [item for sublist in data8 for item in sublist]
    data8 = pd.DataFrame(data8)



data2.to_csv('files/binance_ETHUSDT.csv')
data3.to_csv('files/binance_ADAUSDT.csv')
data5.to_csv('files/bitfinex_ETHUSDT.csv')
data6.to_csv('files/bitfinex_ADAUSDT.csv')
data7.to_csv('files/huobi_BTCUSDT.csv')
data8.to_csv('files/huobi_BTCUSDT.csv')


