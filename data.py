import pandas as pd
import numpy as np
import functions as fn
import os

def data_open(filename):
    default_route = 'files/'
    data = pd.read_csv(default_route + filename)
    df = fn.dataframe(data)
    df_eff_spread = fn.eff_spread(data)
    return df, df_eff_spread
def get_file_names(directory_path):
    # Obtener la lista de nombres de archivos y directorios en el directorio especificado
    all_entries = os.listdir(directory_path)
    # Filtrar solo los archivos (excluir directorios)
    file_names = [entry for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry))]
    return file_names
def consumir_orderbooks(data_files):
    dataframes = {}
    effective_spreads = {}

    for file_name in data_files:
        base_name = file_name.split('.')[0]
        df, eff_spr = data_open(file_name)

        dataframes[base_name] = df
        effective_spreads[base_name] = eff_spr
    return dataframes,effective_spreads
