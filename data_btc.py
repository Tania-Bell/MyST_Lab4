import functions as fn
import pandas as pd
import asyncio

if __name__ == "__main__":
    exchange1 = ["binance"]
    run_time = 3600  # seconds
    symbol1 = "BTC/USDT"
    #symbol2 = "ETH/USDT"
    #symbol3 = "ADA/USDT"



    exchange2 = ["bitfinex"]

    data4 = asyncio.run(fn.multi_orderbooks(exchange2, run_time=run_time, symbol=symbol1))
    data4 = [item for sublist in data4 for item in sublist]
    data4 = pd.DataFrame(data4)
"""

    data1 = asyncio.run(fn.multi_orderbooks(exchange1, run_time=run_time, symbol=symbol1))
    data1 = [item for sublist in data1 for item in sublist]
    data1 = pd.DataFrame(data1)

    

    data2 = asyncio.run(fn.multi_orderbooks(exchange1, run_time=run_time, symbol=symbol2))
    data2 = [item for sublist in data2 for item in sublist]
    data2 = pd.DataFrame(data2)

    data3 = asyncio.run(fn.multi_orderbooks(exchange1, run_time=run_time, symbol=symbol3))
    data3 = [item for sublist in data3 for item in sublist]
    data3 = pd.DataFrame(data3)

    

    

    data5 = asyncio.run(fn.multi_orderbooks(exchange2, run_time=run_time, symbol=symbol2))
    data5 = [item for sublist in data2 for item in sublist]
    data5 = pd.DataFrame(data5)

    data6 = asyncio.run(fn.multi_orderbooks(exchange2, run_time=run_time, symbol=symbol3))
    data6 = [item for sublist in data3 for item in sublist]
    data6 = pd.DataFrame(data6)
"""

#data1.to_csv('files/binance_BTCUSDT.csv')
#data2.to_csv('files/binance_ETHUSDT.csv')
#data3.to_csv('files/binance_ADAUSDT.csv')
data4.to_csv('files/bitfinex_BTCUSDT.csv')
#data5.to_csv('files/kraken_ETHUSDT.csv')
#data6.to_csv('files/kraken_ADAUSDT.csv')

# este codigo para leer datos: modificalo para que diga la variable y archivo que quieres
# data = pd.read_csv('files/dat.csv')

# este codigo genera los dataframes:
# df = fn.dataframe(data)

# este codigo guarda el dataframe de los volumenes en csv
# df.to_csv('files/data_volumes.csv')

# este codigo es para la tabla de el effective spread
#df_eff_spread = fn.eff_spread(data)

#print(df,df_eff_spread)