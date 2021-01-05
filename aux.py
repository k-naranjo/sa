
import tweepy as tw #Twitter hook
import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
#s%matplotlib inline
from wordcloud import WordCloud,STOPWORDS
import string
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
from sqlalchemy.types import Text

def connect_to_twitter(credentials_path):

	#reads login info
	#f=open("../twitter_credentials.txt","r")
	f=open(credentials_path,"r")
	lines=f.readlines()
	# your Twitter API key and API secret
	my_api_key=lines[1].rstrip("\n")
	my_api_secret=lines[3].rstrip("\n")
	access_token=lines[5].rstrip("\n")
	access_token_secret=lines[7].rstrip("\n")
	f.close()

	# authenticate
	auth = tw.OAuthHandler(my_api_key, my_api_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tw.API(auth, wait_on_rate_limit=True)

	return api

def save_df_to_db(df,database_credentials,table_name):
  f=open(database_credentials,"r")
  lines=f.readlines()
  # your Twitter API key and API secret
  my_host=lines[2].rstrip("\n")
  my_user=lines[1].rstrip("\n")
  my_db=lines[0].rstrip("\n")
  my_password=lines[3].rstrip("\n")
  f.close()

  try:


    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
            .format(host=my_host, db=my_db, user=my_user, pw=my_password))

    df2=df.copy()
    df2['hashtags']=df2.hashtags.astype(str)
    # Convert dataframe to sql table                                   
    df2.to_sql(table_name, engine, if_exists='append', index=False,dtype={'hashtags':Text})
  except Exception as e:
    print("Houston, we've got a problem" +str(e))


def get_tweets(api, search_query, start_date,num_tweets):
  # get tweets from the API
  tweets = tw.Cursor(api.search,
                q=search_query,
                lang="en",
                since=start_date).items(num_tweets)


  # store the API responses in - list third part 
  tweets_copy = []
  for tweet in tweets:
      try:
          tweets_copy.append(tweet)
      except tw.TweepError as e:
          print("Something went wrong")
          print("Tweepy Error: {}".format(e))

  print("Total Tweets fetched:", len(tweets_copy))


  # intialize the dataframe
  tweets_df = pd.DataFrame()

  # populate the dataframe
  for tweet in tweets_copy:
      hashtags = []
      try:
          for hashtag in tweet.entities["hashtags"]:
              hashtags.append(hashtag["text"])
          text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
      except:
          pass
      tweets_df = tweets_df.append(pd.DataFrame({
                                                 'tweet_id': tweet.id,
                                                 'user_id':tweet.user.id,
                                                 'user_name': tweet.user.name, 
                                                 'user_location': tweet.user.location,
                                                 'user_description': tweet.user.description,
                                                 'user_verified': tweet.user.verified,
                                                 'date': tweet.created_at,
                                                 'text': text, 
                                                 'hashtags': [hashtags if hashtags else None],
                                                 'source': tweet.source
                                                 }))
      tweets_df = tweets_df.reset_index(drop=True)
  return tweets_df


def clean_word(data):
    #words = " ".join(data['tweet'])
    words = " ".join(data['text'])
    
    cleaned_words = " ".join([word for word in words.split() 
                             if 'http' not in word
                             and not word.startswith('@')
                             and not word.startswith('#')
                             and word != 'RT'])
    return cleaned_words



def wcloud(cleaned_words,word_cloud_name, word_cloud_caption):
  wordcloud = WordCloud(stopwords=STOPWORDS,
                        background_color='black',
                        width=3000,
                        height=2500
                        ).generate(cleaned_words)

  print('vaccine tweets')

  plt.figure(1,figsize=(12,12))
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.title(word_cloud_caption)
  #plt.show()
  plt.savefig(word_cloud_name + '.png')


def preprocess_tweet_text(tweet):
	tweet.lower()
	# Remove urls
	tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
	# Remove user @ references and '#' from tweet
	tweet = re.sub(r'\@\w+|\#','', tweet)
	# Remove punctuations
	tweet = tweet.translate(str.maketrans('', '', string.punctuation))
	# Remove stopwords
	#tweet_tokens = word_tokenize(tweet)
	#filtered_words = [w for w in tweet_tokens if not w in stop_words]
	return tweet

def dict_converter(dict1):
  dictlist = list()
  for key, value in dict1.items():
    temp = [key,value]
    dictlist.append(temp)
  return dictlist

def sa_tweets(tweets_df,image_path,image_title):
	
	#preprocess tweets
	tweets_df['cleaned_text']=tweets_df['text'].apply(preprocess_tweet_text)

	# show the dataframe
	#tweets_df.head()
	sid = SentimentIntensityAnalyzer()

	tweets_df['neg']=0.0
	tweets_df['neu']=0.0
	tweets_df['pos']=0.0
	tweets_df['compound']=0.0


	for i in range(len(tweets_df)): 
	  aux_list=dict_converter(sid.polarity_scores(tweets_df.loc[i,'cleaned_text']))
	  tweets_df.loc[i,'neg']=aux_list[0][1]
	  tweets_df.loc[i,'neu']=aux_list[1][1]
	  tweets_df.loc[i,'pos']=aux_list[2][1]
	  tweets_df.loc[i,'compound']=aux_list[3][1]
	  print("compound score is "+ str(aux_list[3][1]))

	print(tweets_df[['cleaned_text','compound']])


	num_pos=len(tweets_df[tweets_df.compound>0])
	num_neg=len(tweets_df[tweets_df.compound<0])
	print ("positive tweets: "+str(num_pos))
	print ("negative tweets: "+str(num_neg))


	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	classification = ['Positive Tweets', 'Negative Tweets']
	scores = [num_pos,num_neg]
	ax.bar(classification,scores, color=['red', 'green' ])
	#plt.show()

	plt.title(image_title)
	#plt.show()
	plt.savefig(image_path + '.png')

	return tweets_df


