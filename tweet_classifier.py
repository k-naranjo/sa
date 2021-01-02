
import tweepy as tw #Twitter hook
import numpy as np # linear algebra
import pandas as pd # data processing
import string
import matplotlib.pyplot as plt
#s%matplotlib inline
from wordcloud import WordCloud,STOPWORDS
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer




#reads login info
f=open("../twitter_credentials.txt","r")
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


search_query = "#vaccine -filter:retweets"

# get tweets from the API
tweets = tw.Cursor(api.search,
              q=search_query,
              lang="en",
              since="2020-12-30").items(10)


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
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source}))
    tweets_df = tweets_df.reset_index(drop=True)

# show the dataframe
print(tweets_df.head())

def preprocess_tweet_text(tweet):
    #tweet.lower()
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

#for tweet in tweets_df:
print(tweets_df['text'])

tweets_df['cleaned_text']=tweets_df['text'].apply(preprocess_tweet_text)

#for tweet in tweets_df:
print(tweets_df['cleaned_text'])

def dict_converter(dict1):
  dictlist = list()
  for key, value in dict1.items():
    temp = [key,value]
    dictlist.append(temp)
  return dictlist

# show the dataframe
tweets_df.head()
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

