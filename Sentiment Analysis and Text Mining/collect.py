#!/usr/bin/env python
# coding: utf-8

# In[56]:


from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
import pickle
import os


# In[57]:


def get_twitter():
    consumer_key = 'tNkGzG2gFIQCfLwBXb8YeclEh'
    consumer_secret = 'kX88kGqkWD7yvpttAP6DtJUrEKnvnn4X2l0kQn7qszK4sYN38N'
    access_token = '1086860929608880133-jsHyGz5fJqKpM5OO6ASTdKGE7FwUU9'
    access_token_secret = 'S9KNFCuvi8EzaCO7fDDE6CL0nPYpBG5MYadUpaQg6p2CF'
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
    print("Connection Established")


# In[58]:


def read_screen_names(filename):
    candidates_file = open(filename,'r')
    return(candidates_file.read().split())


# In[59]:


def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


# In[60]:


def get_users_friends(twitter, screen_names):
    users_list = []
    for sc_name in screen_names:
        request = robust_request(twitter, 'users/lookup', {'screen_name': sc_name}, max_tries=5)
        u = [j for j in request]
        friend_list = []
        request = robust_request(twitter, 'friends/ids', {'screen_name': sc_name, 'count': 5000}, max_tries=5)
        friend_list = sorted([str(j) for j in request])
        r = {'screen_name': u[0]['screen_name'],
             'id': str(u[0]['id']),
             'friend_id': friend_list}
        users_list.append(r)
    return users_list


# In[61]:


def get_tweets(twitter, screen_name, num_tweets):
    r = robust_request(twitter, 'search/tweets', {'q': screen_name, 'count': num_tweets})
    tweets = [j['text'] for j in r]

    return tweets


# In[62]:


def save_obj(obj, name):
    """
    store, list of dicts
    """    
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)


# In[63]:


def main():
    print("Importing Twitter Data----")
    twitter = get_twitter()
    print('Twitter connection built')
    screen_names = read_screen_names('names.txt')
    print('Read screen names:\n%s' % screen_names)
    users = get_users_friends(twitter, screen_names)
    save_obj(users, 'tweets_collected_user')
    print("Tweets collected and saved")
    tweets = get_tweets(twitter, screen_names[0], 100)
    save_obj(tweets, 'tweets_data')
    print("%d tweets available" % (len(tweets)))

if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:




