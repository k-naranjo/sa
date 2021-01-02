
import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
#s%matplotlib inline
from wordcloud import WordCloud,STOPWORDS
from aux import *



api=connect_to_twitter("../twitter_credentials.txt")


search_query = "#vaccine -filter:retweets"
start_date="2020-12-31"
num_tweets=20
tweets_df=get_tweets(api,search_query,start_date,num_tweets)

# show the dataframe
tweets_df.head()


clean_words = clean_word(tweets_df)

#wcloud(clean_words,"experiment2","Graph title")

sa_tweets(tweets_df)