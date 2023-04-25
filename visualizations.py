import plotly.express as px

def plots(dataframe, title): 
    fig=px.line(dataframe, x="timestamp", y="mid_price",color="exchange",title=("Mid price " + title))

    return fig.show()

