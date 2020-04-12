#!/usr/bin/env python
# coding: utf-8

# In[97]:


from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pickle
import re
import numpy as np


# In[98]:


def download_afin():
    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    file = ZipFile(BytesIO(url.read()))
    afinn_data = file.open('AFINN/AFINN-111.txt')
    return afinn_data


# In[99]:


def readFile(file):
    af = {}
    for ll in file:
        l = ll.strip().split()
        if len(l) == 2:
            af[l[0].decode("utf-8")] = int(l[1])
    return af


# In[100]:


def get_tweets(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


# In[101]:


def tokenize(doc, keep_internal_punct=False):
    new_doc = doc.lower()
    if keep_internal_punct == False:
        token = re.sub('\W+', ' ',new_doc).split() 
    if keep_internal_punct == True:
        token = [re.sub('^\W+|\W+$', '', x) for x in new_doc.split()]
    return np.array(token)


# In[102]:


def token_features(tokens, feats):
    rd = Counter(tokens)
    for k in rd:
        feats["token="+k] = rd[k]


# In[103]:


def token_pair_features(tokens, feats, k=3):
    windows = []
    def window_creator(list,degree):
        for ws in range(len(tokens) - degree + 1):
            yield [list[ws+l] for l in range(degree)]

    window_generator = window_creator(tokens,k)

    for window in window_generator:
        subseq = [c[0]+"__"+c[1] for c in combinations(window,2)]
        for sub in subseq:
            if "token_pair="+sub not in feats:
                feats["token_pair="+sub] = 1
            elif "token_pair="+sub in feats:
                feats["token_pair="+sub] = feats["token_pair="+sub] + 1


# In[104]:


positive_tweets = []
negative_tweets = []
neutral_tweets = []


def scores(tweet, afinn):
    credit = 0

    terms = tokenize(tweet)
    
    for t in terms:
        if t in afinn:
            credit += afinn[t]

    if credit > 0:
        positive_tweets.append(tweet)
    if credit < 0:
        negative_tweets.append(tweet)
    if credit == 0:
        neutral_tweets.append(tweet)


# In[105]:


def all_features(tweets, afinn):
    for tweet in tweets:
        scores(tweet, afinn)


# In[106]:


def results(p_tweets, ng_tweets, neu_tweets):
    res = {}
    res['pos'] = p_tweets
    res['neg'] = ng_tweets
    res['neutral'] = neu_tweets

    return res


# In[107]:


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)


# In[108]:


def main():
    afindownload = download_afin()
    afinn = readFile(afindownload)
    print('afinn file downloaded.')
    tweets = get_tweets('tweets_data')
    print('tweets fetched')
    all_features(tweets, afinn)
    print('got sentiment for all tweets.')
    print('There are %d positive tweets, %d negative tweets and %d neutral tweets.' %
          (len(pos_tweets), len(neg_tweets), len(neutral_tweets)))
    cla_ret = results(pos_tweets, neg_tweets, neutral_tweets)
    save_obj(cla_ret, 'classify')


if __name__ == '__main__':
    main()


# In[ ]:




