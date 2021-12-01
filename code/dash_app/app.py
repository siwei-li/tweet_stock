import dash
from dash import Output, Input, dcc
from dash import html

from tabs import tab1, tab2
# from tab2_callbacks import tab2_out, upload_prediction, render_graph2

import flask

server = flask.Flask(__name__) # define flask app.server

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    # dbc.themes.BOOTSTRAP,
    # "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
]
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets)
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



