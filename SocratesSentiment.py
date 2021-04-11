#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import tweepy as tw
import pandas as pd
import googletrans
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# # Set up OAuth Tokens

# In[2]:


consumer_key= 'xxxxxxxx'
consumer_secret= 'xxxxxxxx'
access_token= 'xxxxxxxx'
access_token_secret= 'xxxxxxxx'


# # Authorize

# In[3]:


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# # Extracting Specific Tweets from Twitter

# In[4]:


search_words = "Ivo Rosa -filter:retweets"
date_since = "2021-04-08"
num_tweets = 100

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="pt",
              since=date_since).items(num_tweets)

# Create list of tweets
tweet_list = [tweet.text for tweet in tweets]

# Create pandas data frame with tweets
tweet_text = pd.DataFrame(data=tweet_list,columns=['tweets'])


# # Inspect tweets

# In[5]:


pd.options.display.max_colwidth = 200
tweet_text["tweets"][1]


# # Translate tweets

# In[7]:


translator = Translator()
result = translator.translate('Mitä sinä teet')


# In[8]:


print(result.src)
print(result.dest)
print(result.origin)
print(result.text)
print(result.pronunciation)


# In[ ]:


translations = translator.translate(tweet_text["tweets"][1]).text
translations


# In[ ]:


translator = Translator()
translations = {}
for column in tweet_text.columns:
    # Unique elements of the column
    unique_elements = tweet_text[column].unique()
    for element in unique_elements:
        # Adding all the translations to a dictionary (translations)
        translations[element] = translator.translate(element).text


# In[ ]:


translations


# In[ ]:


translations_df = pd.DataFrame.from_dict(translations, orient='index')
#translations_df.reset_index(inplace = True)
#translations_df = translations_df[0]
#translations_df = translations_df[0]
#translations_df


# # Analyze overall sentiment of each tweet

# In[ ]:


analyzer = SentimentIntensityAnalyzer()
tweetsWithSent = []
for t in translations_df:
   ps = analyzer.polarity_scores(t)
   tweetsWithSent.append({'text':t, 'compound':ps['compound']})


# In[ ]:


tweetsWithSent


# # Create Pandas dataframe and plot results

# In[ ]:


import pandas as pd
tweetdf = pd.DataFrame(tweetsWithSent)
tweetdf.plot.bar(figsize=(15,5),width=1)
