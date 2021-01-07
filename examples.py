#############################################################################################
#1

#Pull data directly from Twitter

api=connect_to_twitter("../twitter_credentials.txt")

search_for="#vaccine"
search_query = search_for + " -filter:retweets"
start_date="2021-01-04"
num_tweets=200
tweets_df=get_tweets(api,search_query,start_date,num_tweets)


#############################################################################################
#2 CSV

# #save to csv file
tweets_df.to_csv('../data/tweets_'+search_for+'_'+start_date+'.csv', index = True

############################################################################################
#3 MySQL database

# save to database
save_df_to_db(tweets_df,"../database_credentials.txt","tweets_"+search_for)

############################################################################################
#4 Read data

#Pull tweets from csv file
tweets_df2=pd.read_csv("../data/tweets_#vaccine_2021-01-04.csv")

############################################################################################
#5 Word cloud

#clean words for word clouds
clean_words = clean_word(tweets_df)
#create word cloud and save image
wcloud(clean_words,"experiment3","Vaccine word cloud - 2021-01-04")


############################################################################################
#6 Sentiment Analysis

#run sentiment analysis classifier
tweets_df=sa_tweets(tweets_df,"vaccine_2021-01-04","Vaccine mentions (2021-01-04)")
