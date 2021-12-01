import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dcc
from dash import html

from utils import get_price_df

price_df = get_price_df("AAPL")

layout = html.Div(id="tab1",
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
                                  html.Div([
                                      dcc.Upload(
                                          id='upload-data',
                                          children=html.Div(id="file-hint"),
                                          multiple=True,
                                          style={
                                              'width': '100%',
                                              'font-size': '11px',
                                              'height': '50px',
                                              'lineHeight': '50px',
                                              'borderWidth': '1px',
                                              'borderStyle': 'dashed',
                                              'borderRadius': '5px',
                                              'textAlign': 'center',
                                              'margin': '10px'
                                          },
                                      ),
                                      dbc.Button(
                                          "Import .csv data",
                                          className="collapse-button", id="import",
                                          # style={"margin-top": "5px", "margin-left": "0"}
                                          style={"height":"40px", "margin-top": "15px"},
                                          n_clicks=0
                                      ),
                                      dbc.Popover(
                                          html.P(id="popover1"),
                                          target="import",
                                          trigger="click", style={"margin-left": "20px","font-size":"13px"}, )
                              ],
                                      style={"display": "flex",
                                             "justify-content": "left","margin-left":"-10px"})
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
