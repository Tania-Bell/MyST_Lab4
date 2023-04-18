
# Exchanges: binance, bitget, bitmart

ccxt.exchanges



async def importdata(exchange_id,symbol):
    orderbook = Non
    exchange = getattr(ccxta, exchange_id)()
    time_1 = time.time()
    time_f = 0
    ob = []
    while time_f <= run_time:
        try:
            await exchange.market(symbol)
            orderbook = await exchange.fetch_order_book(market["symbol"])
            datetime = exchange.iso8601(exchange.milliseconds())
            # unpack values
            ask_price, ask_size =np.array(list(zip(*orderbook["asks"]))[0:2])
            bid_price, bid_size = np.array(list(zip(*orderbook["bids"]))[0:2])
            spread = np.round(ask_price - bid_price, 4)
            # Final data format for the results
            ob.append(
                {
                    "exchange":exchange_id,
                    "datetime":datetime,
                    "orderbook":{
                                "ask_size":ask_size.tolist(),
                                "ask":ask_price.tolist(),
                                "bid":bid_price.tolist(),
                                "bid_size":bid_size.tolist(),
                                "spread":spread.tolist()
                    },
                }
            )
            # End time
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
        except Exception as e:
            time_2 = time.time()
            time_f = round(time_2 - time_1, 4)
            print(type(e.__name__,str(e)))
    await exchange.close()
    return ob

async def multi_orderbooks(exchanges, run_time: int, symbol: int):
    input_coroutines = [
        async_importdata(exchange, run_time, symbol) for exchange in exchanges
    ]
    orderbooks = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return orderbooks

