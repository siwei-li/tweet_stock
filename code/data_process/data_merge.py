import time
import timeit

import numpy
from textblob import TextBlob
import re
import pandas as pd
import datetime as dt
from pysentimiento import SentimentAnalyzer
from pysentimiento.preprocessing import preprocess_tweet


companies = [ "GOOG", "GOOGL", "MSFT", "TSLA"]
# companies = ["AAPL", "AMZN"]
intervals = ["30m", "60m"]
# intervals = ["60m"]
tweet_lag = 5

analyzer = SentimentAnalyzer(lang="en")
def cleanUpTweet(txt):
    txt = re.sub(r"@[A−Za−z0−9 ]+", "", txt)
    txt = re.sub(r"#", "", txt)
    txt = re.sub(r"RT ", "", txt)
    txt = re.sub(r"https?:\/\/[A−Za−z0−9\.\/]+", "", txt)
    txt = re.sub(r"www.+", "", txt)
    txt = re.sub(r"pic.twitter.com/+", "", txt)
    txt = preprocess_tweet(txt, lang="en", shorten=2)
    return txt


def getOutput(txt):
    return analyzer.predict(txt)


def getProb(output):
    return output.probas[output.output]


def getTextSubjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity


# def getTextPolarity (output):
# return TextBlob(txt).sentiment.polarity

def getTextClass(output):
    return output.output


# def getTextAnalysis(a):
#     if a<0:
#         return "Negative"
#     elif a == 0:
#         return "Neutral"
#     else :
#         return "Positive"

def prepare_twitter_variables(twitter_data):
    results = twitter_data.copy()
    results["clean_text"] = results["body"].apply(cleanUpTweet)
    results["prob"] = results["clean_text"].apply(getOutput).apply(getProb)
    # results["subjectivity"] = results["clean_text"].apply(getTextSubjectivity)
    results["tweet_class"] = results["clean_text"].apply(getOutput).apply(getTextClass)
    return results


def add_twitter_variables(company, interval):
    print("start")
    ########################################
    # Set ups
    ########################################
    # stock_data = pd.read_parquet(f"./kaggle_data/prices_{company}.parquet").iloc[-100:]
    stock_data = pd.read_csv(f"../finance/{interval}_{company}_191001_191231.csv", sep=',').iloc[:-10:]
    t_int = int(interval[:-1])
    results = stock_data.copy()
    results['<TIME>'] = pd.to_datetime(stock_data["<TIME>"], format="%Y%m%d%H%M%S")

    twitter_data = pd.read_csv(f"../kaggle_data/added_tweets_{company}_191001_191231.csv")
    twitter_data['post_date'] = pd.to_datetime(twitter_data['post_date'],  unit='s')
    print(twitter_data.head)

    # twitter_data = pd.read_csv(f"../kaggle_data/tweets_{company}_191001_191231.csv")
    # twitter_data = prepare_twitter_variables(twitter_data)
    # twitter_data = pd.to_csv(f"../kaggle_data/tweets_{company}_191001_191231.csv", index=False)
    # print(twitter_data)

    results["tw_count"] = "NA"
    # results["tw_mean"] = "NA"
    # results["tw_max"] = "NA"
    # results["tw_min"] = "NA"
    # results["tw_vola"] = "NA"
    # results["tw_pola"] = "NA"
    # results["tw_subj"] = "NA"

    results["tw_mean_chars"] = 0

    results["tw_n_pos"] = 0
    results["tw_ratio_pos"] = 0
    results["tw_n_neg"] = 0
    results["tw_ratio_neg"] = 0

    for i in range(0, stock_data.shape[0]):
        if i % 100 == 1:
            print(i)
        current_time = results.iloc[i, :]["<TIME>"]
        # current_time = dt.datetime.strptime(str(stock_data.iloc[i, :]["<TIME>"]), "%Y%m%d%H%M%S")
        # current_time = pd.to_datetime(stock_data.iloc[i, :]["<TIME>"], "%Y%m%d%H%M%S")

        cond1 = twitter_data["post_date"] < (current_time + dt.timedelta(minutes=t_int - tweet_lag))
        cond2 = twitter_data["post_date"] >= (current_time - dt.timedelta(minutes=tweet_lag))
        # print(current_time)
        # print(current_time + dt.timedelta(minutes=t_int - tweet_lag), current_time - dt.timedelta(minutes=tweet_lag))

        # subset twitter data with time range
        twitter_subset = twitter_data.loc[cond1 & cond2, :].copy().reset_index(drop=True)
        # print(twitter_subset.head, twitter_subset.shape)
        # twitter_subset = twitter_data.loc[twitter_data["post_date"]==current_time, :].copy().reset_index(drop=True)

        results.loc[i, "tw_count"] = twitter_subset.shape[0]

        # # set ups for variables calculated afterwards
        # tweets_per = pd.Series(numpy.zeros(t_int))
        # for x in numpy.arange(1, t_int + 1, 1):
        #     scond1 = twitter_subset["post_date"] >= (current_time + dt.timedelta(minutes=int(x) - 1 - tweet_lag))
        #     scond2 = twitter_subset["post_date"] < (current_time + dt.timedelta(minutes=int(x) - tweet_lag))
        #     print(current_time, current_time + dt.timedelta(minutes=int(x) - 1 - tweet_lag), (current_time + dt.timedelta(minutes=int(x) - tweet_lag)))
        #     tweets_per[x - 1] = twitter_subset.loc[scond1 & scond2, :].shape[0]
        #     print(tweets_per[x - 1])
        #
        # results.loc[i, "tw_mean"] = tweets_per.mean()
        # results.loc[i, "tw_vola"] = tweets_per.var()
        # results.loc[i, "tw_min"] = tweets_per.min()
        # results.loc[i, "tw_max"] = tweets_per.max()

        twitter_subset["tw_chars"] = twitter_subset["body"].str.len()
        results.loc[i, "tw_mean_chars"] = twitter_subset["tw_chars"].mean()

        ########################################
        # Content related variables
        ########################################
        # results.loc[i, "tw_pola"] = twitter_subset["polarity"].mean()
        # results.loc[i, "tw_subj"] = twitter_subset["subjectivity"].mean()
        # results.loc[i, "tw_prob"] = twitter_subset["prob"].mean()
        results.loc[i, "tw_n_pos"] = twitter_subset.loc[twitter_subset["tweet_class"] == "POS", :].shape[0]
        results.loc[i, "tw_n_neg"] = twitter_subset.loc[twitter_subset["tweet_class"] == "NEG", :].shape[0]
        if twitter_subset.shape[0]:
            results.loc[i, "tw_ratio_pos"] = results.loc[i, "tw_n_pos"] / twitter_subset.shape[0]
            results.loc[i, "tw_ratio_neg"] = results.loc[i, "tw_n_neg"] / twitter_subset.shape[0]

    return results


if __name__ == "__main__":
    # company = "AAPL"
    # start = time.time()
    # # twitter_data = pd.read_csv(f"../kaggle_data/tweets_{company}_191001_191231.csv", nrows=100)
    # twitter_data = pd.read_csv(f"../kaggle_data/tweets_{company}_191001_191231.csv")
    # print(time.time() - start)
    # twitter_data = prepare_twitter_variables(twitter_data)
    # print(time.time() - start)
    # twitter_data.to_csv(f"../kaggle_data/added_tweets_{company}_191001_191231.csv", index=False)
    # print(time.time() - start)

    # print(twitter_data)

    for company in companies:
        start = time.time()
        # twitter_data = pd.read_csv(f"../kaggle_data/tweets_{company}_191001_191231.csv", nrows=100)
        twitter_data = pd.read_csv(f"../kaggle_data/tweets_{company}_191001_191231.csv")
        print(time.time() - start)
        twitter_data = prepare_twitter_variables(twitter_data)
        print(time.time() - start)
        twitter_data['post_time'] = pd.to_datetime(twitter_data['post_date'], unit='s')
        twitter_data.to_csv(f"../kaggle_data/added_tweets_{company}_191001_191231.csv", index=False)
        print(time.time() - start)
        # for interval in intervals:
            # add_twitter_variables(company, interval).to_csv(f"merged_{company}_{interval}_191001_191231.csv",
            #                                                 index=False)
