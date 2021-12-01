import dash_bootstrap_components as dbc
from dash import Output, Input
from dash import html

from components import generate_table
from tab2 import merged_60m, df2_60m, df2_30m, merged_30m

from app import app

df2_columns = ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>', 'tw_count', 'tw_mean_chars', 'tw_n_pos',
               'tw_ratio_pos', 'tw_n_neg', 'tw_ratio_neg']
dt2_columns = ['<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>', 'Tweet count', 'Tweet mean characters',
               '# of positive tweets', 'Ratio of positive tweets', '# of negative tweets', 'Ratio of negative tweets']


@app.callback(Output('tab2-table', 'children'), Output('buy-sell', 'children'), Output('save-button', 'children'),
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
        buy_sell = "buy 🔺 📈" if pred >= last_real else "sell 🔻 📉"
        if index >= 1:
            advice = f"Last fetched stock value is {last_real:.4f}, predicted value for {time} is {pred:.4f}, the " \
                     f"algorithm suggests to {buy_sell} "

        if advice:
            button = html.Div([dbc.Button(
                "Save Prediction Result",
                className="collapse-button",
                id='click-target'
            ), dbc.Popover(
                html.P(id="popover"),
                target="click-target",
                trigger="click", style={"margin-left": "10px"}, )])

    return generate_table(merge_info, df2_columns, dt2_columns), advice, button


@app.callback(Input(''), Input(''),Output('popover','children'))
def upload_prediction():
    pass
    # if ==200:
    #     return "Prediction and related info saved to database :)"
    # else:
    #     return "Upload error..."

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
