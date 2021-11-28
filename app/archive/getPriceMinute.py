import requests

response = requests.get(
        "https://eodhistoricaldata.com/api/intraday/AAPL.US?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX&interval=1h\
        &from=1569913200&to=1577865600"
    )