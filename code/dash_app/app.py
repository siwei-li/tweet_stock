import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import requests
from dash import Output, Input, dcc
from dash import html

from app.dash_app import tab1, tab2

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
# dbc.themes.BOOTSTRAP,
# "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Tweet the Stocks"




app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Tweet the Stocks", className="header-title"),
                html.P(
                    children="Explore the correlation of stock prices and the related tagged tweets in 2019",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    dcc.Tabs(id="tabs", value='tab1', children=[
                        dcc.Tab(label='Historical records', value='tab1', ),
                        dcc.Tab(label='Prediction', value='tab2'),
                    ], colors={
                        "border": "white",
                        "primary": "#e36209",
                        "background": "#fafbfc"
                    })),
            ],
            className="tabs",
        ),
        tab1.layout,
        tab2.layout,

    ]
)


@app.callback(
    Output('tab1', 'style'), Output('tab2', 'style'),
    [Input('tabs', 'value')])
def show_hide_tab(tab):
    if tab == 'tab1':
        return {'display': 'block'}, {'display': 'none'}
    elif tab == 'tab2':
        return {'display': 'none'}, {'display': 'block'}







df2_columns = ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>', 'tw_count', 'tw_mean_chars', 'tw_n_pos',
               'tw_ratio_pos', 'tw_n_neg', 'tw_ratio_neg']
dt2_columns = ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>', 'Tweet count', 'Tweet mean characters',
               '# of positive tweets', 'Ratio of positive tweets', '# of negative tweets', 'Ratio of negative tweets']


@app.callback(Output('tab2-table', 'children'), Output('buy-sell', 'children'), Output('save-button','children'),\
              Input('radio-item', "value"), Input("tab2-fig", "clickData"))
def tab2_out(interval, clickData):
    merge_info = merged_60m
    advice = ""
    button = ""
    if interval == "60m":
        df2 = df2_60m
        merged = merged_60m.iloc[355:]
    else:
        df2 = df2_30m
        merged = merged_30m[662:]
    if "points" in clickData and clickData["points"]:
        index = clickData["points"][0]["pointIndex"]
        time = clickData["points"][0]["x"]
        # print(time, merged.iloc[index]['<TIME>'])
        merge_info = merged[merged['<TIME>'].str.startswith(time)]
        # print(merge_info)
        # print(index)
        last_real = df2.iloc[index - 1]['real']
        pred = df2.iloc[index]['pred']
        base = df2.iloc[index]['base']
        buy_sell = "buy 🔺 📈" if pred >= last_real else "sell 🔻 📉"
        if index >= 1:
            advice = f"Last fetched stock value is {last_real:.4f}, predicted value for {time} is {pred:.4f}, the algorithm suggests to {buy_sell}"

        if advice:
            button = html.Div([dbc.Button(
                "Save Prediction Result",
                className="collapse-button",
                id='click-target'
            ), dbc.Popover(
            html.P(id="popover"),
            target="click-target",
            trigger="click", style={"margin-left":"10px"}, )])

    return generate_table(merge_info, df2_columns, dt2_columns), advice, button

@app.callback(Input(''), Input(''),Output('popover','children'))
def upload_prediction():

    if ==200:
        return "Prediction and related info saved to database :)"
    else:
        return "Upload error..."


@app.callback(Output('candle-fig', 'figure'), Input('company-filter', "value"))
def render_graph1(ticker):
    price_df = get_price_df(ticker)

    return go.Figure(data=[go.Candlestick(x=price_df['day_date'],
                                          open=price_df['open_value'],
                                          high=price_df['high_value'],
                                          low=price_df['low_value'],
                                          close=price_df['close_value'])],
                     layout=go.Layout(margin=dict(t=30, b=30, l=50, r=30, pad=5)))


@app.callback(Output('tab2-fig', 'figure'), Output('mse', 'children'), Input('radio-item', "value"))
def render_graph2(interval):
    if interval == "60m":
        df2 = df2_60m
        merged = merged_60m[355:]
        msg = "Mean Squared Error(MSE) is 3.75e-04, baseline MSE without Tweet analysis is 5.48e-04"
    else:
        df2 = df2_30m
        merged = merged_30m[662:]
        msg = "Mean Squared Error(MSE) is 2.59e-04, baseline MSE without Tweet analysis is 4.26e-04"
    fig2 = go.Figure(data=[
        go.Line(x=merged['<TIME>'], y=df2['real'], mode='lines+markers', line={'dash': 'dash'},
                name='Real stock values')
    ],
        layout=go.Layout(clickmode="event+select"))
    fig2.add_trace(go.Scatter(x=merged['<TIME>'], y=df2['pred'],
                              mode='lines+markers', line={'dash': 'dash'},
                              name='Prediction with Tweets analysis'))
    fig2.add_trace(go.Scatter(x=merged['<TIME>'], y=df2['base'],
                              mode='lines+markers', line={'dash': 'dash'},
                              name='Prediction without Tweets analysis'))
    fig2.update_layout(
        margin=dict(t=30, b=15, l=50, r=15, pad=5))
    return fig2, msg


if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True, port=8080)
    # app.run_server(debug=False, port=8080)
