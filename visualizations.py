import plotly.express as px

def grafica_btc(dataframe): 
    fig=px.line(dataframe, x="timestamp", y="mid_price",color="exchange",title=(" Midprice de BTC/USDT"))

    return fig.show()



def grafica_eth(dataframe): 
    fig=px.line(dataframe, x="timestamp", y="mid_price",color="exchange",title=(" Midprice de ETH/USDT"))

    return fig.show()