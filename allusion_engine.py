#!/usr/bin/env python
# coding: utf-8

# ## Querying Database

# In[1]:


import sqlite3
connection = sqlite3.connect("wiki_clean.db")
cursor = connection.cursor()


# In[2]:


def query_db(target,dedup=True):
    """
    query sqlite database containing allusions based on a target word
    """
    #print(target)
    cursor.execute("SELECT * FROM allusions WHERE target=?", (target,))
    rows = cursor.fetchall()
    if dedup==False:
        return list(set(rows))
    else:
        total  = list(set(rows))
        deduped_allusions = []
        used_cores = []
        for al in total:
            if al[2] not in used_cores:
                used_cores.append(al[2])
                deduped_allusions.append(al)
        return deduped_allusions
        

query_db("comprise")[:4]


# ## Formatting Allusions

# In[3]:


import random


# In[4]:


def format_allusion(allusion):
    """
    return what will be printed out
    """
    altype,al1,al2 = allusion[1:4]
    target_pos = allusion[5]
    al1 = al1.upper()
    al2 = al2.upper() if al2!=None else None
    if altype=="v2np":
        if random.random()>.6:
            return "AS %s" % al1
        else:
            return "AS ONCE DID %s" % al2
    elif altype=="of":
        return "%s" % al1
    elif altype=="compound":
        return "%s" % al1
    elif altype=="adj2np":
        return "LIKE %s" % al1
    elif altype in ["acomp","appos"]:
        if target_pos=="ADJ":
            if random.random()>.4:
                return "AS %s" % al1
            else:
                return "AS %s, %s," % (al1,al2)
        elif target_pos=="NOUN":
            if random.random()>.4:
                return al1
            else:
                return "%s, %s," % (al1,al2)
        


# ## Getting Allusions Based on Input

# In[5]:


import spacy
nlp = spacy.load("en_core_web_lg")


# In[6]:


def get_target_and_others(text,n_other=5):
    """
    RETURNS
    ((target,pos),[other_words])
    """
    others = []
    spacied = nlp(text)
    tokens = list(reversed([i for i in list(spacied.sents)[-1]]))
    tokens = [t for t in tokens if t.pos_!="PUNCT"]
    target = tokens[0]
    return ((str(target).lower(),target.pos_),[str(i) for i in tokens[1:n_other+1]])
    
get_target_and_others("I like you. you are my friend. I remain")


# In[7]:


import random


# In[8]:


def get_n_from_possibilities(possibilities,target_pos,others,n=5,used_cores=[]):
    """
    get n possible allusions
    prioritizing those that have matching ancillary words
    and then those with the correct POS
    """
    #print(possibilities[0][5])
    to_return = []
    possibilities = [p for p in possibilities if p[2] not in used_cores]
    best = [p for p in possibilities if (p[5]==target_pos and p[4]!=None and bool(set(others) & set(p[4].split("|"))))]
    mid = [p for p in possibilities if (p[5]==target_pos and p not in best)]
    worst = [p for p in possibilities if p not in best+mid]
    ## now choose
    for group in [best,mid,worst]:
        if len(group)>0:
            to_return += random.sample(group,min(n,len(group)))
            if len(to_return)==n:
                break
    return to_return
        


# In[9]:


def prep_allusion(allusion,target):
    """
    return a dictionary of data for the interface
    """
    return {"ready_allusion":format_allusion(allusion),"core_allusion":allusion[2],"article":allusion[6],"target":target}


# In[10]:


with open('custom_stopwords.txt','r') as f:
    stops = [i.rstrip('\n') for i in f.readlines() if i.startswith("##")==False]


# In[11]:


max_len_of_allusion = 140 ## for not returning really long allusions


# In[12]:


def get_allusions_for_text(text,n=5,used_cores=[]):
    """
    main function, what the interface will query
    used_cores|
    """
    target_tup,others = get_target_and_others(text)
    #print(target_tup)
    target,target_pos = target_tup
    if target in stops: ## don't return for stopwords
        return []
    #print( target,others)
    possibilities = query_db(target)
    possibilities = [p for p in possibilities if len(p[2])<max_len_of_allusion]
    allusions = get_n_from_possibilities(possibilities,target_pos,others,n,used_cores)
    #print(allusions)
    allusions = [prep_allusion(a,target) for a in allusions]
    
    return allusions
    
get_allusions_for_text("I like you. you are my friend. I remain a distressed nomadic people")


# `used_cores` helps with deduplication.

# In[14]:


get_allusions_for_text("I like you. you are my friend. I remain a distressed nomadic people",used_cores=["of the South"])


# ***
