import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import requests
from dash import Output, Input, dcc
from dash import dash_table
from dash import html

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

base_url = "https://dsci551-sl-default-rtdb.firebaseio.com/"
headers = {'accept': 'application/json'}


def get_price_df(ticker):
    # price_df = pd.read_csv(f'../kaggle_data/prices_{ticker}.csv')
    response = requests.get(url=base_url + f'prices_{ticker}.json', headers=headers)
    assert response.status_code == 200
    price_df = pd.DataFrame(response.json())
    price_df.sort_values(by='day_date', ascending=True, inplace=True)
    return price_df


def get_tweet_df(ticker):
    # df = pd.read_csv(f'../data_process/page1_{ticker}.csv',
    #                  usecols=['post_time', 'body', 'comment_num', 'retweet_num', 'like_num', 'total_engagement',
    #                           'prob', 'tweet_class'])
    response = requests.get(url=base_url + f'page1_{ticker}.json', headers=headers)
    assert response.status_code == 200
    df = pd.DataFrame(response.json())
    df = df[['post_time', 'body', 'total_engagement', 'comment_num', 'retweet_num', 'like_num',
             'tweet_class', 'prob']]
    return df


df_columns = ['post_time', 'body', 'total_engagement', 'comment_num', 'retweet_num', 'like_num', \
              'tweet_class', 'prob']
dt_columns = ['Posted On', 'Tweet Body', 'Total Engagement', 'Comments', 'Retweets', 'Likes', \
              'Tweet Sentiment', 'Probability']


def generate_table(df, df_columns=df_columns, dt_columns=dt_columns):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": col, "id": df_columns[idx]} for idx, col in enumerate(dt_columns)],
        data=df.to_dict('records'),
        # style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[
            {'if': {'column_id': 'body'},
             'width': '50%'},
            {'if': {'column_id': 'post_time'},
             'width': '11%'},
            {'if': {'column_id': '<TIME>'},
             'width': '11%'},
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_cell={
            'textAlign': 'left',
            'padding':"3px",
            # 'height':'auto',
            'minHeight':"20px",
            'maxHeight':"60px",
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None,
        page_action='native',
        page_current=0,
        page_size=10,
    )


price_df = get_price_df("AAPL")

df2_30m = pd.read_csv("../data_process/page2_30m.csv")
df2_60m = pd.read_csv("../data_process/page2_60m.csv")
merged_30m = pd.read_csv("../data_process/merged_AAPL_30m_191001_191231.csv")
merged_60m = pd.read_csv("../data_process/merged_AAPL_60m_191001_191231.csv")
fig2 = go.Figure(data=[
    go.Line(x=merged_30m.iloc[662:]['<TIME>'], y=df2_30m['real'], mode='lines+markers', line={'dash': 'dash'},
            name='Real stock values')
],
    layout=go.Layout(clickmode="event+select"))
fig2.add_trace(go.Scatter(x=merged_30m.iloc[662:]['<TIME>'], y=df2_30m['pred'],
                          mode='lines+markers', line={'dash': 'dash'},
                          name='Prediction with Tweets analysis'))
fig2.add_trace(go.Scatter(x=merged_30m.iloc[662:]['<TIME>'], y=df2_30m['base'],
                          mode='lines+markers', line={'dash': 'dash'},
                          name='Prediction without Tweets analysis'))
fig2.update_layout(
    margin=dict(t=30, b=15, l=50, r=15, pad=5))

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

        html.Div(id="tab1",
                 style={'display': 'block'},
                 children=[
                     html.Div(id="dropdowns", children=[
                         html.Div(
                             children=[
                                 html.Div(children="Company", className="menu-title"),
                                 dcc.Dropdown(
                                     id="company-filter",
                                     options=[
                                         {"label": "Apple ($AAPL)", "value": "AAPL"},
                                         {"label": "Amazon ($AMZN)", "value": "AMZN"},
                                         {"label": "Alphabet ($GOOG)", "value": "GOOG", 'disabled': True},
                                         {"label": "Google ($GOOGL)", "value": "GOOGL", 'disabled': True},
                                         {"label": "MSFT ($MSFT)", "value": "MSFT", 'disabled': True},
                                         {"label": "TSLA ($TSLA)", "value": "TSLA", 'disabled': True},

                                     ],
                                     value="AAPL",
                                     clearable=False,
                                     className="dropdown",
                                 ),
                                 dbc.Button(
                                     "Import .csv data",
                                     className="collapse-button", id="import", style={"margin-top":"5px", "margin-left":"0"}
                                 ),
                             ]
                         ),

                         html.Div(
                             children=[
                                 html.Div(children="Filter tweets by sentiment", className="menu-title"),
                                 dcc.Dropdown(
                                     id="type-filter",
                                     options=[
                                         {"label": "Positive", "value": "POS"},
                                         {"label": "Negative", "value": "NEG"},
                                         {"label": "Neutral", "value": "NEU"},
                                         {"label": "All", "value": "all"},
                                     ],
                                     value="all",
                                     clearable=False,
                                     searchable=False,
                                     className="dropdown",
                                 ),
                             ],
                         ),
                         html.Div(
                             children=[
                                 html.Div(
                                     children="Filter by Date",
                                     className="menu-title"
                                 ),
                                 dcc.DatePickerSingle(
                                     id="date-picker",
                                     date="2019-10-01",
                                     min_date_allowed="2019-10-01",
                                     max_date_allowed="2019-12-30",
                                     # start_date="2019-01-01",
                                     # end_date="2019-12-30",
                                     className="dropdown",
                                 ),
                             ]
                         ),
                     ],
                              className="menu",
                              ),

                     html.H3(id="graph1-title",
                             children="Historical prices: click on me to show tweets posted on each day :)",
                             className="graph-title"),

                     html.Div(id='tab1-graph',
                              children=dcc.Graph(
                                  id="candle-fig",
                                  figure=
                                  go.Figure(data=[go.Candlestick(x=price_df['day_date'],
                                                                 open=price_df['open_value'],
                                                                 high=price_df['high_value'],
                                                                 low=price_df['low_value'],
                                                                 close=price_df['close_value'])],
                                            layout=go.Layout(margin=dict(t=30, b=30, l=50, r=30, pad=5))),
                                  clickData={})
                              ),

                     html.Div([html.P(id="tweet-cnts", className="card-text")],

                              style={"margin": "10px", "padding": "10px",
                                     'border-style': 'solid',
                                     'border-width': '1px',
                                     'border-color': '#1f78b4',
                                     'color': '#1f78b4',
                                     'border-radius': '10px',
                                     'background-color': 'white'},

                              ),

                     html.Div(className="table",
                              children=[
                                  html.P(id="type-cnts",
                                         className="table-title"),

                                  html.Div(id='tab1-table')])
                 ]

                 )
        ,
        html.Div(id="tab2",
                 style={'display': 'none'},
                 children=[
                     html.Div(
                         html.Div(id="radios", children=[

                             html.Div(children=[html.H4(id="radio-title",
                                                        children="Aggregate tweets by: ",
                                                        className="radio-title"),
                                                dcc.RadioItems(
                                                    id="radio-item",
                                                    options=[
                                                        {'label': '30-minute interval', 'value': '30m'},
                                                        {'label': '60-minute interval', 'value': '60m'},
                                                    ],
                                                    value='30m',
                                                    style={'padding-top': '22px',
                                                           # 'width': '50%'
                                                           },
                                                    labelStyle={
                                                        'margin': '5px',
                                                        'padding': '5px',
                                                    }
                                                ), ],
                                      className="radio-items"
                                      ),
                             html.P(id="mse", className="table-title"),
                         ],
                                  className="radio",
                                  ), style={"margin": "10px auto", "padding-bottom": "10px", "width": "60%",
                                            'border-style': 'solid',
                                            'border-width': '1px',
                                            'border-color': '#1f78b4',
                                            'color': '#1f78b4',
                                            'border-radius': '10px',
                                            'background-color': 'white'
                                            }),

                     html.H3(id="graph2-title",
                             children="Investment suggestion: click on me to show investment idea on each given point in time",
                             className="graph-title"),

                     html.Div(id='tab2-graph',
                              children=dcc.Graph(
                                  id="tab2-fig",
                                  figure=fig2,
                                  clickData={})
                              ),

                     html.Div(id="buy-sell",
                              className="table-title", style={"font-size":"18px", "margin":"20px"}),
                     html.Div(id="save-button",
                              className="table-title", style={"margin-left":"-5px"}),

                     html.Div(className="table",
                              children=[
                                  html.P(id="tab2-info-title",
                                         children="Infomation of merged Tweets",
                                         className="table-title"),

                                  html.Div(id='tab2-table')])
                 ]

                 )

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


def get_time_rows(tweet_df, my_key):
    return tweet_df[tweet_df['post_time'].str.startswith(my_key)]


def get_type_rows(tweet_df, my_key):
    if my_key == "all":
        return tweet_df
    return tweet_df[tweet_df['tweet_class'] == my_key]


@app.callback(Output('tab1-table', 'children'), Output('tweet-cnts', 'children'), Output('type-cnts', 'children'), \
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


# @app.callback(Input(''), Input(''),Output('popover','children'))
# def upload_prediction():
#
#     if ==200:
#         return "Prediction and related info saved to database :)"
#     else:
#         return "Upload error..."


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
