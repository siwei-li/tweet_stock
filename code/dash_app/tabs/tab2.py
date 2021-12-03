import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html

df2_30m = pd.read_csv("./data/page2_30m.csv")
df2_60m = pd.read_csv("./data/page2_60m.csv")
merged_30m = pd.read_csv("./data/merged_AAPL_30m_191001_191231.csv")
merged_60m = pd.read_csv("./data/merged_AAPL_60m_191001_191231.csv")

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

layout = html.Div(id="tab2",
                  style={'display': 'none'},
                  children=[
                      dcc.Store(id='local-store', storage_type='local'),
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
                               className="table-title", style={"font-size": "18px", "margin": "20px"}),
                      html.Div(id="save-button",
                               className="table-title", style={"margin-left": "-5px"}),

                      html.Div(className="table",
                               children=[
                                   html.P(id="tab2-info-title",
                                          children="Infomation of merged Tweets",
                                          className="table-title"),

                                   html.Div(id='tab2-table')])
                  ]

                  )
