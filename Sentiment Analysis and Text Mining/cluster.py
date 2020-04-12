#!/usr/bin/env python
# coding: utf-8

# In[239]:


from collections import Counter, defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pickle 
import math
from itertools import chain, combinations


# In[240]:


def readFile(name):
     with open(name + '.pkl', 'rb') as val:
        return pickle.load(val)


# In[241]:


def print_num_friends(users):
    for i in users:
            print(i['screen_name'] + ' ' +str(len(i['friend_id'])))


# In[242]:


def count_friends(users):
    d = Counter()
    friend_list = []
    for r in users:
        friend_list.append(r['friend_id'])
    for u in friend_list:
        d.update(u)
    return d


# In[243]:


def friend_overlap(users):
    h = 0
    jk = []
    cc = tuple()
    
    for i in range(0, len(users)):
        for j in range(i+1, len(users)):
            for m in range(0, len(users[i]['friend_id'])):
                for n in range(0, len(users[j]['friend_id'])):
                    if users[i]['friend_id'][m] == users[j]['friend_id'][n]:
                        h += 1
            cc = (users[i]['screen_name'], users[j]['screen_name'], h)
            jk.append(cc)
            h = 0

    jk = sorted(jk, key=lambda tup: (-tup[2], tup[0], tup[1]))

    return jk


# In[244]:


def create_graph(users, friend_counts, min_common):
    f = [x1 for x1 in friend_counts if friend_counts[x1] > min_common]
    graph = nx.Graph()
    for x1 in f:
        graph.add_node(x1)
    for m in users:
        graph.add_node(m['id'])
        g = set(m['friend_id']) & set(f)
        for d in g:
            graph.add_edge(d, m['id'])

    nx.draw_networkx(graph, with_labels=True)
    
    return graph


# In[245]:


def draw_network(graph, users, filename):
    ll = {}
    for n1 in graph.nodes():
        for uc in users:
            if n1 in uc['id']:
                ll[n1] = uc['screen_name']
    
    plt.figure(figsize=(15, 15))
    plt.axis('off')

    nx.draw_networkx(graph, labels=ll, alpha=.5, node_size=100, width=.5)
    plt.savefig(filename)


# In[246]:


def get_subgraph(graph, min_degree):
    sn = []
    nodes = graph.nodes()
    for n in nodes:
        if graph.degree(n) >= min_degree:
            sn.append(n)
    subgraph = graph.subgraph(sn)

    return subgraph


# In[247]:


def bfs(graph, root, max_depth):
    node2distances = {}
    node2num_paths = {}
    node2parents = {}
    q = deque([])
    seen = deque([])

    
    node2distances[root] = 0
    node2num_paths[root] = 1
    q.append(root)
    seen.append(root)

    
    while len(q) != 0:
        current = q.popleft()
        seen.append(current)
        
        if node2distances[current] >= max_depth:
            break
        else:
            for n in graph.neighbors(current):
                if not (n in seen):
                    #new leaf
                    if not (n in q):
                        node2distances[n] = node2distances[current] + 1
                        node2parents[n] = [current]
                        node2num_paths[n] = len(node2parents[n])
                        q.append(n)
                    
                    elif n in q and node2distances[n] != node2distances[current]:
                        node2parents[n].append(current)
                        node2num_paths[n] = len(node2parents[n])

    return node2distances, node2num_paths, node2parents


# In[248]:


def bottom_up(root, node2distances, node2num_paths, node2parents):
    ns = defaultdict(float)
    abc = defaultdict(float)
    
    for k in node2distances.keys():
        if k != root:
            ns[k] = 1.0
        else:
            ns[root] = 0.0
            
    result = sorted(node2distances.items(), key=lambda x: (-x[1]))
    
    for k, v in result:
        if k != root:
            n1 = node2parents[k]
            len_parent = len(n1)
            if len_parent == 0:
                break
            if len_parent == 1:
                ns[n1[0]] = ns[n1[0]] + ns[k]
                e = tuple(sorted([k, n1[0]]))
                abc[e] = ns[k]
            else:
                edge_score = ns[k]/len_parent
                for p in n1:
                    ns[p] = ns[p] + edge_score
                    edge = tuple(sorted([k, p]))
                    abc[edge] = edge_score
    
    return dict(sorted(abc.items()))


# In[249]:


def approximate_betweenness(graph, max_depth):
    edgescore = defaultdict(float)
    b = defaultdict(float)
    
    for node in graph.nodes():
        node2distances, node2num_paths, node2parents = bfs(graph, node, max_depth)
        result = bottom_up(node, node2distances, node2num_paths, node2parents)
        
        for k, v in result.items():
            edgescore[k] += v
        
    for k, v in edgescore.items():
        b[k] = edgescore[k]/ 2.0   
    return dict(sorted(b.items()))


# In[250]:


def partition_girvan_newman(graph, max_depth, num_clusters):
    cs = []

    partition_edge = list(sorted(approximate_betweenness(graph, max_depth).items(), key=lambda x:(-x[1], x[0])))
    
    for i in range(0, len(partition_edge)):
        graph.remove_edge(*partition_edge[i][0])
        cs = list(nx.connected_component_subgraphs(graph))
        if len(cs) >= num_clusters:
            break

    
    new_cs = [cluster for cluster in cs if len(cluster.nodes()) > 1]

    return new_cs, graph


# In[251]:


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)


# In[252]:


def main():
    users = readFile('tweets_collected_user')
    print("users info got.")
    print('Number of friends of each user:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    
    graph = create_graph(users, friend_counts, 0)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'original.png')
    print('network drawn to original.png')

    subgraph = create_graph(users, friend_counts, 1)
    print('subgraph has %s nodes and %s edges' % (len(subgraph.nodes()), len(subgraph.edges())))
    draw_network(subgraph, users, 'pruned.png')
    print('network drawn to pruned.png')
    
    clusters, partitioned_graph = partition_girvan_newman(subgraph, 5, 100)

    save_obj(clusters, 'clusters')

    draw_network(partitioned_graph, users, 'clusters.png')
    print('network drawn to clusters.png')


if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:




