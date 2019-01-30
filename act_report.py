#!/usr/bin/env python
# coding: utf-8

# # Analysis

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


twitr_clean_df=pd.read_csv('/home/workspace/image_predctns/twitter_archive_master.csv')


# In[3]:


twitr_clean_df.info()


# In[4]:


twitr_ana_df=twitr_clean_df[['timestamp','rating_numerator','rating_denominator',
                             'retweets','favourites']].copy()

twitr_ana_df.info()


# In[ ]:





# In[5]:


twitr_ana_df['rating_obtained']=twitr_ana_df['rating_numerator']/twitr_ana_df['rating_denominator']


twitr_ana_df.rating_obtained.value_counts()


# In[6]:


# set the timestamp as index to get the time display in plots against
# the rating obtained
twitr_ana_df.set_index(twitr_ana_df['timestamp'],inplace=True)


# In[23]:


twitr_ana_df['rating_obtained'].plot()
plt.ylim(0,5)

plt.ylabel('ratio')
plt.xticks(rotation=90)
plt.show()


# So now we see that the ratings are mostly ranging around from 0 to 1 except for few occassions where the rating happened exorbitantly high by few users. Maybe they were extremely happy or so and did that.
# 
# 

# In[8]:


twitr_ana_df.plot(kind='scatter',x='favourites',y='retweets')
plt.xlabel('Favourites')
plt.ylabel('Retweets')
plt.title('Scatterplot Of Favourites and Retweets')
plt.show()


# The scatter plot shows that the retweets and favourites have strong positive correlation, meaning if a tweet is liked then it is most likely that it will be retweeted too.

# In[24]:


twitr_ana_df['retweets'].plot(color='red',label='Retweeted')
twitr_ana_df['favourites'].plot(color='green',label='Favourited')
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend()
plt.show()


# We can see that the favourited numbers are generally more than the retweets.

# In[ ]:




