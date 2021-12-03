from dash import dash_table


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