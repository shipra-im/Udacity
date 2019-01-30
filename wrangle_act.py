#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import requests
import matplotlib.pyplot as plt


# In[2]:


ls


# Data Gathering::
# 1)twitter-archive-enhanced.csv is, available so downloaded as given.
# 2)image-predictions.tsv is gathered using url
# 3)used the available tweet-json.txt file(JSON method used to fetch data) to create a dataframe "tweet_json_df" having retweet,favurite and tweetid info.

# In[3]:


twitr_archv_enhncd_df=pd.read_csv('twitter-archive-enhanced.csv')


# In[4]:


twitr_archv_enhncd_df.head()


# In[5]:


twitr_archv_enhncd_df.info()


# In[6]:


# getting secong file using url response request method
response=requests.get('https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv')


# In[7]:



urls='https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response


# In[8]:


folder_name='image_predctns'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
with open(os.path.join(folder_name,urls.split('/')[-1]),mode='wb') as file:
    file.write(response.content)


# In[9]:


ls


# In[10]:


cd image_predctns


# In[11]:


ls


# In[12]:


image_pred_df=pd.read_csv('/home/workspace/image_predctns/image-predictions.tsv',sep='\t')


# In[13]:


image_pred_df.head()


# In[14]:


image_pred_df.info()


# In[ ]:





# In[15]:


import tweepy


# In[16]:


#consumer_key='ship_gup'
#consumer_secret='01011986'
#access_token='1985'
#access_secret='imshipra'
#consumer_key = 'HIDDEN'
#consumer_secret = 'HIDDEN'
#access_token = 'HIDDEN'
#access_secret = 'HIDDEN'


# In[17]:


#auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
#auth.set_access_token(access_token,access_secret)


# In[18]:


#api=tweepy.API(auth)


# In[19]:


#api.get_status(892420643555336193, tweet_mode='extended')


# Created my developer app but still got the invalid token error so going to use the provided json text and python file
# 

# In[20]:


#df_tweet_json_list=[]
import json

df_list=[] 

with open('/home/workspace/tweet-json.txt', 'r') as json_file:
    for line in json_file:
        tweet = json.loads(line)
        df_list.append({'tweet_id': tweet['id'],
                        'retweets': tweet['retweet_count'],
                        'favourites': tweet['favorite_count']})
tweet_json_df = pd.DataFrame(df_list, columns = ['tweet_id', 'retweets', 'favourites'])


# In[21]:


tweet_json_df.head()


# In[22]:


tweet_json_df.info()


# In[23]:


twitr_archv_enhncd_df.info()


# In[24]:


twitr_archv_enhncd_df.in_reply_to_status_id.value_counts()


# In[25]:


twitr_archv_enhncd_df[twitr_archv_enhncd_df.name.apply(len) < 3]


# In[26]:


twitr_archv_enhncd_df.rating_numerator.value_counts()


# In[27]:


twitr_archv_enhncd_df.rating_denominator.value_counts()


# In[28]:


twitr_archv_enhncd_df.retweeted_status_id.value_counts()


# In[29]:


#(image_pred_df['jpg_url'].values=='').sum()
image_pred_df['jpg_url'].value_counts(dropna=False)


# In[30]:


image_pred_df.info()


# In[31]:


image_pred_df[image_pred_df['jpg_url']=='https://pbs.twimg.com/media/Co-hmcYXYAASkiG.jpg']


# In[32]:


tweet_json_df.info()


# In[33]:


len(tweet_json_df['tweet_id'].unique().tolist())


# In[ ]:





# In[ ]:





# # Quality Issue
# twitr_archv_enhncd_df table has several issues such as ::
# 
# 
# a)names are not defined properly for few like 79 dogs.
# 
# 
# b)in_reply_to_status_id,retweeted_status_id,retweeted_status_user_id,in_reply_to_user_id are defined as float variables. They shall be either int/string type.
# 
# 
# c)timestamp,retweeted_status_timestamp are defined as objects rather they shall be datetime.
# 
# 
# d)rating_numerator has values less than 10 and rating_denominator has values more than 10, since we have standardization against denom being equal to 10 and numerator being more than 10 we need clean up this issue too.
# 
# 
# e)display full content of text column
# 
# 
# f)sources are difficult to read i.e, full text is not visible.
# 
# g) few rows tweets are not for dogs rather for some another animal like polar bear or so.
# 
# 
# table image_pred_df has issues such as ::
# 
# 
# a)data is missing in this table i.e, 2075 rows than expected as 2356.
# b)same jpg url is for 2 tweet ids that means we have retweets too in the dataset.
# 
# 
# tweet_json_df table has::
# 2 rows are less than the twitter_archv_enhncd_df table which means we have missing info in this table too.
# 
# 

# # Tidyness Issue
# 1) Image_pred_df table has jpg_url and image_num we can use them to merge in table twitr_archv_enhncd_df
# 
# 
# 2)retweet_count and favourite_count of tweet_json_df table can also be added in twitr_archv_enhncd_df based on tweet_id no need for separate tables.

# # Cleaning Code

# In[34]:


#copy dataframes
twitr_clean_df=twitr_archv_enhncd_df.copy()
image_clean_df=image_pred_df.copy()
jstweet_clean_df=tweet_json_df.copy()


# In[35]:


twitr_clean_df.info()


# # Define
# putting data in one table rather spreaded in 3 diff tables

# # Code

# In[36]:



twitr_clean_df=pd.merge(left=twitr_clean_df,right=jstweet_clean_df,on ='tweet_id'
                        ,how='left')


# In[37]:


twitr_clean_df.info()


# In[38]:


image_clean_df.info()


# In[39]:


twitr_clean_df=pd.merge(left=twitr_clean_df,right=image_clean_df,
                       on='tweet_id',how='left')


# # Test

# In[40]:


twitr_clean_df.info()


# In[41]:


##checking for duplicate tweets
twitr_clean_df.duplicated().sum()


# # Define
# Cleaning issue of text and source string not visible fully

# # Code

# In[42]:


#fixing the issue of setting column width to get the text and source 
#displayed fully in the window
twitr_clean_df['text'].map(len).max()


# In[43]:


#setting the length according to the maximum text length
pd.options.display.max_colwidth = 180


# # Test

# In[44]:


twitr_clean_df


# 

# # Define
# melt the columns like pupper,floofer,doggo,puppo in different dog stage 

# # Code

# In[45]:


twitr_clean_df.info()


# In[46]:


# Select the columns to melt and to remain
MELTS_COLUMNS = ['doggo', 'floofer', 'pupper', 'puppo']
STAY_COLUMNS = [x for x in twitr_clean_df.columns.tolist() if x not in MELTS_COLUMNS]

twitr_clean_df=pd.melt(twitr_clean_df,STAY_COLUMNS,value_vars=MELTS_COLUMNS,
                      var_name='stages',value_name='dog_stage')


# # Test

# In[47]:


twitr_clean_df=twitr_clean_df.drop('stages',axis=1)


# In[48]:


twitr_clean_df.info()


# # Define
# Removing the duplicated rows based on tweet_id,jpg_url and unwanted columns like retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp

# # Code

# In[49]:


#Removing the duplicated rows
twitr_clean_df=twitr_clean_df.drop_duplicates()


# In[50]:


#Delet tweets with no jpg_url
twitr_clean_df=twitr_clean_df.dropna(subset=['jpg_url'])


# In[51]:


#delete the retweets as we dont need them
twitr_clean_df=twitr_clean_df[pd.isnull(twitr_clean_df.retweeted_status_id)]


# In[52]:


#delete the columns which are not needed
twitr_clean_df=twitr_clean_df.drop('retweeted_status_id',1)
twitr_clean_df=twitr_clean_df.drop('retweeted_status_user_id',1)
twitr_clean_df=twitr_clean_df.drop('retweeted_status_timestamp',1)


# In[53]:


#drop the the rows where there are no expanded urls
twitr_clean_df=twitr_clean_df.dropna(subset=['expanded_urls'])


# In[54]:



sum(twitr_clean_df['expanded_urls'].isnull())


# # Test

# In[55]:


twitr_clean_df.info()


# In[56]:


twitr_clean_df.head()


# # Define
# Issue to remove the tweet rows which are not for dogs rating rather people have sent for some other animal.

# # Code

# In[57]:


# after removing duplicates lets remove the rows which are not for the dogs tweets
twitr_clean_df=twitr_clean_df[~twitr_clean_df['text'].astype(str).str.contains("We only rate dogs",na=False)]

twitr_clean_df=twitr_clean_df[~twitr_clean_df['text'].astype(str).str.contains("only send dogs",na=False)]
twitr_clean_df=twitr_clean_df[~twitr_clean_df['text'].astype(str).str.contains("only rate dogs",na=False)]
twitr_clean_df=twitr_clean_df[~twitr_clean_df['text'].astype(str).str.contains("not a dog",na=False)]
twitr_clean_df=twitr_clean_df[~twitr_clean_df['text'].astype(str).str.contains('non-canines',na=False)]


# # Define
# find out the ratings where we have denominator less than 10 and change them to 10

# # Code

# In[58]:


twitr_clean_df=twitr_clean_df.replace(twitr_clean_df[twitr_clean_df['rating_denominator']!=10] ,10)                      


# # Test
# 

# In[59]:


twitr_clean_df[twitr_clean_df['rating_denominator']!=10]


# # Define
# tweets have same jpg_urls so lets drop extra tweets for same images
# 
# 

# In[60]:


twitr_clean_df['jpg_url'].value_counts(dropna=False)


# # Code

# In[61]:


twitr_clean_df=twitr_clean_df.drop_duplicates(['jpg_url'])


# # Test

# In[62]:


twitr_clean_df.info()
twitr_clean_df['jpg_url'].value_counts(dropna=False)


# # Define
# changing the timestamp to dattime datatype

# # Code

# In[64]:


twitr_clean_df['timestamp']=pd.to_datetime(twitr_clean_df['timestamp'],errors='coerce')


# # Test

# In[65]:


twitr_clean_df.info()


# In[66]:


twitr_clean_df.head()


# # Define
# change the data type of in_reply_to_status_id and in_reply_to_user_id to string data type

# # Code

# In[67]:


twitr_clean_df['in_reply_to_status_id']=twitr_clean_df['in_reply_to_status_id'].astype('str')
twitr_clean_df['in_reply_to_user_id']=twitr_clean_df['in_reply_to_user_id'].astype('str')


# In[68]:


twitr_clean_df.info()


# # Save

# In[ ]:


twitr_clean_df.to_csv('twitter_archive_master.csv')


# In[ ]:




