# Implementación de funciones Via MAIN
import data as dt
import functions as ft
import visualizations
data_files = dt.get_file_names("files") # Abriendo Información de los orderbooks observados
# Procesado de orderbooks
series, effective_spreads = dt.consumir_orderbooks(data_files)
# Se pueden acceder a partir de la clave del exchange_pareja, ejemplo
# series["binance_BTCUSDT"]
series["binance_BTCUSDT"]
effective_spreads["binance_BTCUSDT"]
series["binance_ADAUSDT"]
effective_spreads["binance_ADAUSDT"]
series["binance_ETHUSDT"]
effective_spreads["binance_ETHUSDT"]
series["bitfinex_BTCUSDT"]
effective_spreads["bitfinex_BTCUSDT"]
series["bintfinex_ADAUSDT"]
effective_spreads["bintfinex_ADAUSDT"]
series["bintfinex_ETHUSDT"]
effective_spreads["bintfinex_ETHUSDT"]


