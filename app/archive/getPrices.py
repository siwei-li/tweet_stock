import datetime

import yfinance as yf
from datetime import date

ticker_list = ["AAPL"]
path = "../finance/"
file_name = "AAPL"
# start_date = '2021-10-01'
# last_date = '2021-10-02'
last_date = date.today().strftime('%Y-%m-%d')
start_date = (date.today() - datetime.timedelta(days=59)).strftime('%Y-%m-%d')

for interval in ["30m","1h"]:
    stock_data = yf.download(ticker_list,start=start_date , end=last_date , interval=interval)
    stock_data.to_csv(path + file_name + "_" + start_date + "_" + last_date + "_" + interval + ".csv")