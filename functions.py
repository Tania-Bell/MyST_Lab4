import asyncio
import ccxt.async_support as ccxta
import ccxt
import time
import numpy as np
import pandas as pd
import ast


async def async_client(exchange_id, run_time: int, symbol: str):
    orderbook = None
    exchange = getattr(ccxta, exchange_id)()
    time_1 = time.time()
    time_f = 0
    ob = []
    while time_f <= run_time:
        try:
            await exchange.load_markets()
            market = exchange.market(symbol)
            orderbook = await exchange.fetch_order_book(market["symbol"])
            ohlcv = await exchange.fetch_ohlcv(market["symbol"], limit=1)
            closing_price = ohlcv[-1][4]
            datetime = exchange.iso8601(exchange.milliseconds())
            # Unpack values
            ask_price, ask_size = np.array(list(zip(*orderbook["asks"]))[0:2])
            bid_price, bid_size = np.array(list(zip(*orderbook["bids"]))[0:2])
            spread = np.round(ask_price - bid_price, 6)
            mid_price = np.round((ask_price[0] + bid_price[0]) / 2, 6)
            vwap = np.round(((ask_price * ask_size).sum() + (bid_price * bid_size).sum()) / (ask_size.sum() + bid_size.sum()), 6)
            levels=len(ask_price)
            # Final data format for the results
            ob.append(
                {
                    "exchange": exchange_id,
                    "datetime": datetime,
                    "orderbook": {
                        "ask_size": ask_size.tolist(),
                        "ask": ask_price.tolist(),
                        "bid": bid_price.tolist(),
                        "bid_size": bid_size.tolist(),
                        "spread": spread.tolist(),
                        "closing_price": closing_price,
                        "mid_price": mid_price,
                        "vwap": vwap,
                        "levels":levels
                    },
                }
            )
            # End time
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
        except Exception as e:
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
            print(type(e).__name__, str(e))
    await exchange.close()
    return ob


async def multi_orderbooks(exchanges, run_time: int, symbol: str):
    input_coroutines = [
        async_client(exchange, run_time, symbol) for exchange in exchanges
    ]
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return orderbooks

def dataframe(data):
    df = pd.DataFrame(columns=['exchange', 'timestamp', 'levels', 'ask_volume', 'bid_volume', 'total_volume', 'mid_price', 'vwap'])
    for row in range(len(data)):
        ob = ast.literal_eval(data['orderbook'][row])
        df.loc[row, 'exchange'] = data['exchange'][row]
        df.loc[row, 'timestamp'] = data['datetime'][row]
        df.loc[row, 'levels'] = ob['levels']
        df.loc[row, 'ask_volume'] = sum(ob['ask_size'])
        df.loc[row, 'bid_volume'] = sum(ob['bid_size'])
        df.loc[row, 'total_volume'] = sum(ob['ask_size']) + sum(ob['bid_size'])
        df.loc[row, 'mid_price'] = ob['mid_price']
        df.loc[row, 'vwap'] = ob['vwap']
    return df

def eff_spread(data):
    df = pd.DataFrame(columns=['timestamp', 'close', 'spread', 'effective spread'])
    for row in range(len(data)):
        ob = ast.literal_eval(data['orderbook'][row])
        df.loc[row, 'timestamp'] = data['datetime'][row]
        df.loc[row, 'close'] = 0 #poner close
        df.loc[row, 'spread'] = 0 #poner el spread
        df.loc[row, 'effective spread'] = 0 #poner effectice pread
    return df