#!/usr/bin/env python
# coding: utf-8

# In[80]:


import pickle


# In[81]:


def readFile(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)   


# In[82]:


def avg_num_clusters(clusters):
    t = 0
    for cluster in clusters:
        t += len(cluster.nodes())
    ave = t / len(clusters)
    return ave


# In[83]:


def main():
    text_file = open('summary.txt', 'w')
    users = readFile('tweets_collected_user')
    text_file.write("Number of screen_names  are %d  \n" % (len(users)))
    text_file.write('\n')    
    
    text_file.write("All friends of these users are also collected for future analysis.\n")
    for user in users:
        text_file.write("%s has %d friends.\n" % (user['screen_name'], len(user['friend_id'])))
    text_file.write('\n')
    tweets = readFile('tweets_data')
    text_file.write('Number of messages collected: %d\n' % (len(tweets)))
    text_file.write('\n')
    
    text_file.write('For sentiment analysis, we collected %d tweets/messages (max. tweets allowed)\n' % (len(tweets)))
    text_file.write('\n')
    clusters =readFile('clusters')
    text_file.write('Number of communities discovered: %d  \n'% (len(clusters)))
    text_file.write('\n')
    t=0
    for cluster in clusters:
        t += len(cluster.nodes())
    text_file.write('Total number of users in the communities are: %d' % t)  
    text_file.write('\n')
    text_file.write('We cluster all initial users and their friends in to different communities and exclude users that followed by less than two initial users and outliers.\n')
    text_file.write('Outliers are those points that clustered as singleton.\n')
   
    text_file.write("There are %d communities\n" % (len(clusters)))
    text_file.write('\n')
    a_n_clusters = avg_num_clusters(clusters)
    text_file.write('Average number of users per community: %d\n' % (a_n_clusters))
    text_file.write('\n')
    text_file.write('Number of instances per class found are following:\n')
    text_file.write('\n')
    text_file.write('There are three classes for sentiment analysis.\n')
    classify_results = readFile('classify')
    text_file.write('The positive class has %d instances\n' % (len(classify_results['pos'])))
    text_file.write('The negative class has %d instances\n' % (len(classify_results['neg'])))
    text_file.write('The neutral class has %d instances\n' % (len(classify_results['neutral'])))
    text_file.write('\n')
    text_file.write('One example from each class:\n')
    text_file.write('\n')
    text_file.write('Positive example:\n%s\n' % (classify_results['pos'][0]))
    text_file.write('Negative example:\n%s\n' % (classify_results['neg'][0]))
    text_file.write('Neutral example:\n%s\n' % (classify_results['neutral'][0]))
    print('Write to summary.txt done.')
if __name__ == '__main__':
    main()    


# In[ ]:




