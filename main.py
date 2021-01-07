
import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
#s%matplotlib inline
from wordcloud import WordCloud,STOPWORDS
from aux import *



#######################################################################
#Pull data directly from Twitter

api=connect_to_twitter("../twitter_credentials.txt")

search_for="#vaccine"
search_query = search_for + " -filter:retweets"
start_date="2021-01-01"
until_date="2021-01-02"
num_tweets=20
tweets_df=get_tweets(api,search_query,start_date,until_date,num_tweets)

#print(tweets_df[['date']]) #date verification
# show the dataframe
#tweets_df.head()

#clean words for word clouds
#clean_words = clean_word(tweets_df)
#create word cloud and save image
#wcloud(clean_words,"trial1","Vaccine word cloud - "+start_date)

#run sentiment analysis classifier
tweets_df=sa_tweets(tweets_df,"vaccine_"+start_date,"Vaccine mentions ("+start_date+")")

#save to csv file
#tweets_df.to_csv('../data/tweets_'+search_for+'_'+start_date+'.csv', index = True)

# #save to database
# #save_df_to_db(tweets_df,"../database_credentials.txt","tweets_"+search_for)


########################################################################
#Pull tweets from csv file

#tweets_df2=pd.read_csv("../data/tweets_#vaccine_2021-01-04.csv")
#print(tweets_df2.head())

#word cloud
#clean words for word clouds
#clean_words2 = clean_word(tweets_df2)
#create word cloud and save image
#wcloud(clean_words2,"read_experiment","Vaccine word cloud 2- 2021-01-04")


#run sentiment analysis classifier
#tweets_df2=sa_tweets(tweets_df2,"vaccine_image_test","Vaccine mentions (2021-01-04)")