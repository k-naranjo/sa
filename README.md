# Twitter scraper for Python
This is a simple API that allows you to get tweets and analyze them in two different forms:

* Get word clouds of the tweets that match your search
* Analyze the sentiment of tweets
* Place the location of tweets on a map :boom:


## What it does
This API allows you to:

* Get tweets from Twitter for a search term (It is possible to choose the tweets' date.)
* Generate a word cloud from a dataframe of tweets and to save it to a file.
* Run a sentiment analysis classifier, get a bar graph of the results, and store the results in a dataframe.
* Save a dataframe of tweets to a MySQL database or a CSV file.
* Read a dataframe of tweets from a CSV file.
* Create a map showing the users' location for all the tweets that include such information.


## How to use it
If you're getting your tweets directly from Twitter, you will have to get developer access and then provide the required info to the code via text file (see example below).

If you have your data stored in a database or a csv file, read it into a dataframe and you're good to go. Please be aware that this implementation expects a `DataFrame` object including a `text` field and a `user_location` field.
### Requirements
In order to use this code you must have the following installed:
* `numpy`
* `pandas`
* `matplotlib.pyplot`

* `nltk` (sentiment classifier)

* `selenium` (map functionality)
* `geocoder` (map functionality)
* `geckodriver` (map functionality)


### Examples

#### Connect to twitter and get tweets matching a search term

```python
api=connect_to_twitter("your_file_location/twitter_credentials.txt")

search_for="pfizer + vaccine"
search_query = search_for + " -filter:retweets"
start_date="2020-01-08"
until_date="2021-01-09" #no tweets on this date or later will be selected
num_tweets=100

tweets_df=get_tweets(api,search_query,start_date,until_date,num_tweets)

```
`tweets_df` is a Pandas DataFrame containing the results.

#### Create a word cloud for tweets
You need a Pandas DataFrame containing a `text` field for the tweet's text.
```python
clean_words = clean_word(tweets_df) # clean words for word clouds

# create word cloud and save image
wcloud(clean_words,"your_file_location/filename","Word Cloud Title")
```
#### Run a sentiment classifier on the dataframe of tweets
You need a Pandas DataFrame containing a `text` field for the tweet's text.
```python
# run sentiment analysis classifier
new_df=sa_tweets(tweets_df,"file_location")
```
`new_df` is an augmented version of `tweets_df` containing 4 additional fields with the results of the classification: `neg`, `neu`, `pos`, and `compound`. The function will also save a bar graph of the results.
#### Create a map of user locations
You need a Pandas DataFrame containing a `user_location` field.
```python
#create a map
create_tweets_map(tweets_df,"image_filename")
```
The resulting map is saved to `image_filename`. There is no need to add an extension, the program does it automatically.
#### Save tweets to a database
```python
#save to database
save_df_to_db(tweets_df,"your_location/database_credentials.txt","location/filename")
```
#### Save tweets to CSV file
```python
# save to csv file
tweets_df.to_csv('filename.csv', index = True)
```
#### Read tweets from a CSV file
```python
tweets_df=pd.read_csv("filename.csv")
```

## To do
- [ ]	Verify the method that saves the tweets to the database.
- [ ]	Write code for loading tweets from database into a dataframe. 
- [ ]	Improve preprocessing for both word clouds and sentiment analysis.
- [ ]	Train my own sentiment classifier.
- [ ]	Work on geospacial analysis (partial work done, there is a map function now :smiley:).