import pandas as pd
import requests

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
    response = requests.get(url=base_url + f'page1_{ticker}.json', headers=headers)
    assert response.status_code == 200
    df = pd.DataFrame(response.json())
    df = df[['post_time', 'body', 'total_engagement', 'comment_num', 'retweet_num', 'like_num',
             'tweet_class', 'prob']]
    return df


def get_time_rows(tweet_df, my_key):
    return tweet_df[tweet_df['post_time'].str.startswith(my_key)]


def get_type_rows(tweet_df, my_key):
    if my_key == "all":
        return tweet_df
    return tweet_df[tweet_df['tweet_class'] == my_key]

def filename_handle(filename, len=20):
    name, extension = filename.split(".")
    return name[:len]+"..."+extension
