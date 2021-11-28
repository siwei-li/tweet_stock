import dash
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


def generate_table(df):
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
            # {'if': {'column_id': 'Region'},
            #  'width': '30%'},
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_cell={
            'textAlign': 'left',
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

df2 = pd.read_csv("../data_process/page2_30m.csv")
times = pd.read_csv("../data_process/merged_AAPL_30m_191001_191231.csv")

tab1 = html.Div(id="tab1-content",
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

                    html.P(id="graph1-title",
                           children="Historical prices: click on me to show tweets posted on each day",
                           className="graph-title"),

                    html.Div(id='tab1-graph',
                             children=dcc.Graph(
                                 id="candle-fig",
                                 figure=
                                 go.Figure(data=[go.Candlestick(x=price_df['day_date'],
                                                                open=price_df['open_value'],
                                                                high=price_df['high_value'],
                                                                low=price_df['low_value'],
                                                                close=price_df['close_value'])]),
                                 clickData={})
                             ),

                    html.P(id="tweet-cnts",
                           className="graph-title"),

                    html.Div(id='tab1-table')
                ]

                )

fig2 = go.Figure(data=[
    go.Line(x=times['<TIME>'], y=df2['real'], mode='lines+markers',line={'dash': 'dash'},
                    name='Real stock values')
],
    layout=go.Layout(clickmode="event+select"))

tab2 = html.Div(id="tab2-content",
                children=[
                    html.Div(id="radios", children=[
                        html.P(id="radio-title",
                               children="Aggregate tweets by: ",
                               className="radio-title"),
                        html.Div(
                            dcc.RadioItems(
                                id="radio-item",
                                options=[
                                    {'label': '30-minute interval', 'value': '30m'},
                                    {'label': '60-minute interval', 'value': '60m'},
                                ],
                                value='30m',
                                # labelStyle={'display': 'inline-block'}
                            ),
                            className="radio-items"
                        ),
                    ],
                             className="radio",
                             ),

                    html.P(id="graph2-title",
                           children="Investment suggestion: click on me to show investment idea on each given point in time",
                           className="graph-title"),

                    html.Div(id='tab2-graph',
                             children=dcc.Graph(
                                 id="tab2-fig",
                                 figure=fig2,
                                 clickData={})
                             ),

                    html.P(id="buy-sell",
                           # children="",
                           className="buy-sell"),

                    html.Div(id='tab2-table')
                ]

                )

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

        html.Div(id="tab-render",
                 children=tab1,
                 className="tab-content",
                 )

    ]
)

fig2.add_trace(go.Scatter(x=times['<TIME>'], y=df2['pred'],
                    mode='lines+markers',line={'dash': 'dash'},
                    name='Prediction with Tweets analysis'))
fig2.add_trace(go.Scatter(x=times['<TIME>'], y=df2['base'],
                    mode='lines+markers',line={'dash': 'dash'},
                    name='Prediction without Tweets analysis'))

@app.callback(dash.dependencies.Output('tab-render', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab1':
        return tab1
    elif tab == 'tab2':
        return tab2


@app.callback(Output('tab1-table', 'children'), Output('tweet-cnts', 'children'), \
              Input('company-filter', "value"), Input("type-filter", "value"), Input("date-picker", "date"),
              Input("candle-fig", "clickData"))
def type_pick(ticker, type, date, clickData):
    tweet_df = get_tweet_df(ticker)
    if "points" in clickData and clickData["points"]:
        date = clickData["points"][0]["x"]
        tweet_df = get_time_rows(tweet_df, date)
    else:
        tweet_df = get_time_rows(tweet_df, date)
    df_f = get_type_rows(tweet_df, type)
    output = {"POS": "positive", "NEG": "negative", "NEU": "neutral", "all": ""}
    return generate_table(df_f), [len(df_f), f" {output[type]}", f" tweets containing ${ticker} found in total on ",
                                  date, "."]


def get_time_rows(tweet_df, my_key):
    return tweet_df[tweet_df['post_time'].str.startswith(my_key)]


def get_type_rows(tweet_df, my_key):
    if my_key == "all":
        return tweet_df
    return tweet_df[tweet_df['tweet_class'] == my_key]


@app.callback(Output('candle-fig', 'figure'), Input('company-filter', "value"))
def render_graph1(ticker):
    price_df = get_price_df(ticker)

    return go.Figure(data=[go.Candlestick(x=price_df['day_date'],
                                          open=price_df['open_value'],
                                          high=price_df['high_value'],
                                          low=price_df['low_value'],
                                          close=price_df['close_value'])])


# @app.callback(Output('tab2-fig', 'figure'), Input('radio-item', "value"))
# def render_graph2(interval):
#     price_df = get_price_df(ticker)
#     # print(ticker)
#
#     return go.Figure(data=[
#         go.Scatter(x=price_df['day_date'], y=price_df['high_value'])
#     ],
#         layout=go.Layout(clickmode="event+select"))


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
    app.config.suppress_callback_exceptions = True
