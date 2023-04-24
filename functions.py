import asyncio
import ccxt.async_support as ccxta
import ccxt
import time
import numpy as np
import pandas as pd
import ast


async def async_client(exchange_id, run_time: int, symbol: str):
    """
    This function returns ask and bid price,
    ask and bid volume, spread, mid price,
    vwap and levels given a list of 
    cryptocurrency trading pairs in 
    a list of exchange markets.

    Parameters
    ---------
    exchange_id : str
        string of exchange markets
    run_time : int
    symbol : str
        string of trading pairs
    Returns
    --------
    ob : dictionary
    """
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
    """
    Uses function async client to create
    orderbooks.
    
    Parameters 
    ----------
    exchanges : str
        string of exchange markets
    run_time : int
    symbol : str
        string of trading pairs
    """
    input_coroutines = [
        async_client(exchange, run_time, symbol) for exchange in exchanges
    ]
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return orderbooks

def dataframe(data):
    """
    Function creates dataframe with information
    of exchange markets and trading pairs.
    
    Parameters
    ----------
    data : DataFrame
    Returns
    ----------
    df : DataFrame
    """
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
    """
    Function creates dataframe of spread
    and effective spread.
    
    Parameters
    ----------
    data : DataFrame
    Returns
    ----------
    df : DataFrame
    """
    df = pd.DataFrame(columns=['timestamp', 'close', 'spread', 'effective spread'])
    def calculate_covariance(x, y):
        return np.cov(x, y)[0][1]

    def calculate_effective_spread(data, window=5):
        closing_prices = [ast.literal_eval(data['orderbook'][row])['closing_price'] for row in range(len(data))]
        price_changes = [closing_prices[i] - closing_prices[i - 1] for i in range(len(closing_prices))]
        price_changes_lag = price_changes[:-window]  # Eliminar los últimos 'window' elementos

        covariance_values = [calculate_covariance(price_changes[i:i + window], price_changes_lag[i:i + window]) for i in range(1, len(price_changes_lag) - window + 1)]


        effective_spread_values = [2 * np.sqrt(abs(cov)) for cov in covariance_values]
        return effective_spread_values

    for row in range(len(data)):
        ob = ast.literal_eval(data['orderbook'][row])
        df.loc[row, 'timestamp'] = data['datetime'][row]
        df.loc[row, 'close'] = ob['closing_price'] # Precio de cierre
        df.loc[row, 'spread'] = np.mean(ob['spread']) # Spread promedio del OB
    eff_spread_list = calculate_effective_spread(data)
    eff_spread_list.extend([np.nan] * abs(len(eff_spread_list) - len(data)))
    df['effective spread'] = eff_spread_list
    df.dropna(inplace=True)
    return df