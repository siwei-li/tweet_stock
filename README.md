# Tweet the Stock

A company's market values are variable and affected by different factors, the most important of which could be the thoughts of the public. We try to analyze the effect of public opinion about a company on that company's market values. 
We are expecting a correlation rate that clarifies the public opinion vs. market values. Sentiment analysis of the Tweets related with certain companies with a time series in a graph might help us with reasoning the possible declines and rises in their stock prices, which also enables making predictions about changes in stock prices as well as providing investors with buy or sell suggestions.

To address the non-linearity and highly complex nature of the underlying process in stock price modeling, we trained a Long-Short-Term-Memory (LSTM) model as our recurrent neural network, which helps to mitigate the issue of exploding or vanishing gradients. To gain better results for tweets’ sentiment classification, we also employed BERT (Bidirectional Encoder Representations from Transformers), a transformer-architecture language model for performing various downstream natural language processing tasks. It is pre-trained from an enormous unlabeled text corpus that encompasses Wikipedia and a comprehensive book corpus and has a deeper sense of language context because of its ability to learn the contextual information bidirectionally. 

Please find more detailed PDF [report](https://github.com/siwei-li/tweet_stock/blob/master/Report.pdf) in the repo.
