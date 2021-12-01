import datetime
from Scweet.scweet import scrape
import pandas as pd


from datetime import date

search_word_list = ["$AAPL"]
last_date = date.today().strftime('%Y-%m-%d')
start_date = (date.today() - datetime.timedelta(days=59)).strftime('%Y-%m-%d')
path = "../tweets/"

data = scrape(words=search_word_list, since="2021-10-01", until="2021-10-02",interval=1, \
              lang="en",
              resume=False)

print(data)
# for search_word in search_word_list:

    # c = twint.Config()
    # c.search = search_word
    # c.Pandas = True
    # twint.run.Search(c)
    # Tweets_df = twint.storage.panda.Tweets_df
    # Tweets_df.to_csv(path + search_word + "_" + start_date + "_" + last_date + ".csv")



# import pandas as pd
#
# from tweepy.api import API
# from tweepy.auth import OAuthHandler
# from tweepy.cursor import Cursor
#
# # Plug in developer account keys
# consumer_key = "ZoGaaYZ67GDr0TurYWv4aHXLN"
# consumer_secret = "IPlIp6O2nDd9gZaugIqfB6fjaGdCPIHevoJS3fx6TTeeNluJgE"
# access_token = "1116849769-LSw3UzWyCNvqxE1PYffAbxhQyOhgVlXnIqbpZIx"
# access_token_secret = "FoPG2ZEQ96szKZFaJXrbQNJymkUWveNQCzkB0GlcMLXvC"
# # bear = "AAAAAAAAAAAAAAAAAAAAAOVtUQEAAAAA%2Fj0c5rWaSPh1afiD7Xa%2B6TweD8s%3DT7INjLcED97ezLZcVj6djgBaTmqFMFfxEJpJZSVGpvvhe1WbbM"
#
# # Give Python your developer account keys
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)  # twitter api set ups
#
# api = API(auth,
#           wait_on_rate_limit=True,
#           # wait_on_rate_limit_notify=True,
#           retry_count=10000,
#           retry_delay=60,
#           timeout=120)
#
# import GetOldTweets3 as got
#
# # Define variables below
# path = ""
# start_date = '2021-10-06'
# last_date = '2021-10-14'
# # search_word_list = ["$AAPL", "AAPL"]
# search_word_list = ["Trump"]
#
# if __name__ == "__main__":
#     # search for each word in search list separately
#     for search_word in search_word_list:
#         print("Current search word: " + search_word)
#         # search for each date separately
#         for date_since in pd.date_range(start=start_date, end=last_date):
#             df = pd.DataFrame([])
#             print(date_since.strftime('%Y−%m−%d'))
#
#             # extract tweets
#             tweets = Cursor(
#                 api,
#                 # api.search,
#                             q=search_word,
#                             extended=True,
#                             lang="en",
#                             until=(date_since + dt.timedelta(days=1)).strftime('%Y−%m−%d'),
#                             # since=date_since.strftime('%Y−%m−%d'),
#                             result_type="recent",
#                             ).items()
#             # print(tweets)
#
#             # tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_word) \
#             #     .setSince(date_since.strftime('%Y−%m−%d'))\
#             #     .setUntil((date_since + dt.timedelta(days=1)).strftime('%Y−%m−%d'))
#             # tweets = got.manager.TweetManager.getTweets(tweetCriteria)
#
#             # put content of object into list
#             users_locs = [[search_word,
#                            # tweet.username,
#                            tweet.user.screen_name,
#                            # tweet.geo,
#                            tweet.user.location,
#                            tweet.text,
#                            # tweet.date
#                            tweet.created_at
#                            ] for tweet in tweets]
#             # make a df
#             tweet_text = pd.DataFrame(data=users_locs,
#                                       columns=["search_word", "user", "location", "text", "date"])
#             # merge the df with the other results for different dates and search words
#             df = df.append(tweet_text)
#             # save daily results
#             df = df.reset_index(drop=True)
#             print(f"{len(df)} Tweets in total.")
#
#             if not df.empty:
#                 df.to_csv(path + search_word + "" + date_since.strftime('%Y−%m−%d') + ".csv")
