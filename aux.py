
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

import geocoder
import os
from selenium import webdriver
import folium
import time




def connect_to_twitter(credentials_path):
  """
  Creates a connection to the Twitter API.

  Given a file containing the Twitter API credentials in 4 separate lines (API key, API secret, access token, and access token secret), it returns a twitter connection object.

  Parameters
  ---------
  credentials_path: str
      the path to a file containing the API info:
      1st line: API key
      2nd line: API secret
      3rd line: access token
      4th line: access token secret

  Returns
  -------
    API (Tweepy Object)
    a connection to the Twitter API object

  """
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
  """
  Saves a dataframe to a database

  Given a Pandas dataframe, a file containing the database credentials and the DB table's name, it updates the table with the information in the dataframe.

  Parameters
  ---------
  df: str
      a Pandas dataframe containing the information to be saved.
      The file must have 4 lines:
      1st line: db name
      2nd line: db user
      3rd line: host
      4th line: password

  """
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


def get_tweets(api, search_query, start_date, until_date,num_tweets):
  """
  Gets tweets from Twitter that match a especific query.

  Given a Twitter connection object, a search term, a start date, and a limit date, it returns a dataframe containing the tweets matching the given criteria. 

  Parameters
  ---------
  api: API (Tweepy object)
      The connection to the Twitter API
  search_query: str
      search term
  start_date: str
      string with start date in YYYY-MM-DD format
  until_date: str
      string with limit date in YYYY-MM-DD format. Tweets posted on this date or after won't be returned.
  num_tweets: int
      Number of tweets to be fetched.

  Returns
  -------
  DataFrame
    a dataframe containing the tweet information:
                        user_name 
                        user_location
                        user_description
                        user_verified
                        date
                        text 
                        hashtags
                        source

  """

  # get tweets from the API
  tweets = tw.Cursor(api.search,
                q=search_query,
                lang="en",
                since=start_date,
                until=until_date).items(num_tweets)


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
  """
  Prepares array of words for word cloud visualization.

  Given a dataframe with a 'text' field, it creates an array of words from which stop words have been removed.

  Parameters
  ---------
  data: DataFrame
      dataframe with field 'text' that includes the text to be processed

  Returns
  -------
    Array
    an array containing all the relevant words for word cloud visualization

  """

  #words = " ".join(data['tweet'])
  words = " ".join(data['text'])
    
  cleaned_words = " ".join([word for word in words.split() 
                           if 'http' not in word
                           and not word.startswith('@')
                           and not word.startswith('#')
                           and word != 'RT'])
  return cleaned_words


def wcloud(clean_words,word_cloud_name, word_cloud_caption):

  """
  generates a word cloud visualization.

  Given an array of words, it creates a word cloud visualization and saves it to a file.

  Parameters
  ---------
  clean_words: Array
      Array of words to be visualized.

  word_cloud_name: str
      wordcloud's filename

  word_cloud_caption: str
      word cloud caption (title)

  """
  wordcloud = WordCloud(stopwords=STOPWORDS,
                        background_color='black',
                        width=3000,
                        height=2500
                        ).generate(clean_words)

  print('vaccine tweets')

  plt.figure(1,figsize=(12,12))
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.title(word_cloud_caption)
  #plt.show()
  plt.savefig(word_cloud_name + '.png')
  plt.close('all')


def preprocess_tweet_text(tweet):
  """
  Preprocess text for the sentiment classifier.

  Given a tweet text in string form, it removes user mentions, hashtags, url, punctuation, and stopwords.

  Parameters
  ---------
  tweet: str
        raw tweet text
  Returns
  -------
    str
    tweet text without user mentions, hashtags, url, punctuation, and stopwords

  """
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
  """
  It converts a dictionary to a list

  Given a dictionary, it returns a list containing the original data.

  Parameters
  ---------
  dict1: Dictionary
        original data in dictionary form
  Returns
  -------
    List
    list containing the original data

  """

  dictlist = list()
  for key, value in dict1.items():
    temp = [key,value]
    dictlist.append(temp)
  return dictlist

def sa_tweets(tweets_df, image_path, image_title):
  """
  apply a sentiment classifier to a dataframe of tweets

  Given a dataframe including a 'text' field, it runs a sentiment classifier 
  and it returns an augmented version of the original dataframe that includes
  the results of the analysis in the fields 'neg', 'neu', pos', and 'compound'.
  It also generates a bar graph of the results.

  Parameters
  ----------
  tweets_df:  DataFrame
              It must include a 'text' field.
  
  image_path: str
              filepath for the bar graph
              
  image_title:str
              image caption

  Returns
  -------
    DataFrame
    a tweets' dataframe including the original fields and the new fields
    'neg', 'neu', pos', and 'compound' that contain the results of the
    analysis.
  """
  tweets_df['cleaned_text']=tweets_df['text'].apply(preprocess_tweet_text)

  #show the dataframe
  #tweets_df.head
  sid=SentimentIntensityAnalyzer()

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

  print(tweets_df[['cleaned_text', 'compound']])

  thres=0.25
  num_pos=len(tweets_df[tweets_df.compound>=thres])
  num_neg=len(tweets_df[tweets_df.compound<=-thres])
  num_neu=len(tweets_df[(tweets_df.compound<thres) & (tweets_df.compound>-thres)])
  
  num_tweets=len(tweets_df.index)
  per_pos=(num_pos/num_tweets)*100
  per_neg=(num_neg/num_tweets)*100
  per_neu=(num_neu/num_tweets)*100
  
  print ("positive tweets: "+str(num_pos))
  print ("negative tweets: "+str(num_neg))
  print ("neutral tweets: "+str(num_neu))

  classification=['Positive', 'Negative', 'Hard to classify/Neutral']
  scores=[num_pos, num_neg, num_neu]
  percentages=[per_pos, per_neg, per_neu]

  y_pos=np.arange(len(classification))
  #plt.bar(y_pos,scores, align='center',  color=['#EE442F', '#00ff00', '#0000ff'])
  plt.bar(y_pos,percentages, align='center',  color=['#ABC3C9', '#E0DCD3', '#CCBE9F'])
  plt.ylabel("Percentage")
  plt.xticks(y_pos, classification)
  plt.title(image_title + '('+str(num_tweets)+' tweets)' )

  plt.savefig(image_path+'.png')
  plt.close('all')
  #plt.show()

  return tweets_df

def create_tweets_map(df, map_path):
	#map creation
	m=folium.Map()


	#add markers
	for i in range(len(df)):
		if df.loc[i,'user_location']!='':
			#give in the normal address we know
			address = geocoder.osm(df.loc[i,'user_location'])
			#add marker to map
			folium.Marker(address.latlng, popup='Statue Of Unity', tooltip='Click Me!').add_to(m)


	# #give in the normal address we know
	# address = geocoder.osm('Columbus, Ohio')
	# #add marker to map
	# folium.Marker(address.latlng, popup='Statue Of Unity', tooltip='Click Me!').add_to(m)


	fn = map_path+'.html' #path to the html file

	# can be defined to fit all points on the map
	#m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
	m.save(fn)

	delay = 2
	tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
	m.save(fn)
	your_browser_path= '/Applications/Firefox.app/Contents/MacOS'
	driver = webdriver.Firefox()
	driver.get(tmpurl)
	#Give the map tiles some time to load
	time.sleep(delay)
	driver.save_screenshot(fn + ".png")
	driver.close()