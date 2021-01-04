
import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
#s%matplotlib inline
from wordcloud import WordCloud,STOPWORDS
from aux import *



api=connect_to_twitter("../twitter_credentials.txt")


search_query = "#vaccine -filter:retweets"
start_date="2020-12-31"
num_tweets=10
tweets_df=get_tweets(api,search_query,start_date,num_tweets)

# show the dataframe
tweets_df.head()

#clean words for word clouds
#clean_words = clean_word(tweets_df)
#create word cloud and save image
#wcloud(clean_words,"experiment2","Graph title")
#run sentiment analysis classifier
tweets_df=sa_tweets(tweets_df,"bar_1","Sentiment")

#tweets_df.to_csv('tweets_test'+start_date+".csv", index = True) 

save_df_to_db(tweets_df,"../database_credentials.txt","tweets")