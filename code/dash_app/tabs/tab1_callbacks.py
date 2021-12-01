import plotly.graph_objs as go
from dash import Output, Input, State
from dash import html

from app import app
from components import generate_table
from utils import get_tweet_df, get_time_rows, get_type_rows, get_price_df, filename_handle


@app.callback(Output('tab1-table', 'children'), Output('tweet-cnts', 'children'), Output('type-cnts', 'children'),
              Input('company-filter', "value"), Input("type-filter", "value"), Input("date-picker", "date"),
              Input("candle-fig", "clickData"))
def type_pick(ticker, type, date, clickData):
    tweet_df = get_tweet_df(ticker)

    if "points" in clickData and clickData["points"]:
        date = clickData["points"][0]["x"]
        tweet_df = get_time_rows(tweet_df, date)
    else:
        tweet_df = get_time_rows(tweet_df, date)
    total_cnts = len(tweet_df)
    pos_cnts = len(get_type_rows(tweet_df, "POS"))
    neg_cnts = len(get_type_rows(tweet_df, "NEG"))
    df_f = get_type_rows(tweet_df, type)
    output = {"POS": "positive", "NEG": "negative", "NEU": "neutral", "all": ""}
    return generate_table(df_f), f"{total_cnts} tweets in total on {date} containing ${ticker}, \
    out of which {pos_cnts / total_cnts * 100:.2f}% ({pos_cnts}) are positive,\
     {neg_cnts / total_cnts * 100:.2f}% ({neg_cnts}) are negative.", f"Displaying {len(df_f)} {output[type]} tweets in total:"


@app.callback(Output('candle-fig', 'figure'), Input('company-filter', "value"))
def render_graph1(ticker):
    price_df = get_price_df(ticker)

    return go.Figure(data=[go.Candlestick(x=price_df['day_date'],
                                          open=price_df['open_value'],
                                          high=price_df['high_value'],
                                          low=price_df['low_value'],
                                          close=price_df['close_value'])],
                     layout=go.Layout(margin=dict(t=30, b=30, l=50, r=30, pad=5)))


@app.callback(Output('popover1', 'children'), Input('import', 'n_clicks'), Input('upload-data', 'contents'))
def hint(clicks, file_content):
    if clicks > 0 and file_content:
        return f"Calculating tweet sentiment scores..."
    return ""


@app.callback(Output('file-hint', 'children'), Input('upload-data', 'contents'),
              State('upload-data', 'filename'), )
def uploaded_files(file_content, filenames):
    if file_content:
        return [filename_handle(filenames[0]),", ",filename_handle(filenames[1])]
    return [
        'Drag and Drop or ',
        html.A('Select Files')
    ]
