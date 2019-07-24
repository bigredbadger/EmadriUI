#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
#from nltk.corpus import stopwords
#import re
#import os
#from pyemd import emd
#from gensim.similarities import WmdSimilarity
#from gensim.models import KeyedVectors
#import sqlite3 as sql

df = pd.read_csv('full.csv')
vect = pickle.load(open('vect.pkl', 'rb'))
#stop_words = stopwords.words('english')
#model_file = os.path.expanduser('~/Desktop/Emadri/GoogleNews-vectors-negative300.bin.gz')
#model = KeyedVectors.load_word2vec_format(model_file, binary = True)
#model.init_sims(replace = True)


def OutfitGenerator(product_id):
    orig_id = df.loc[df['product_id'] == product_id].index[0]
    gender = df.loc[df['product_id'] == product_id]['gender'].item()
    
    similarity = [0] * len(df.index)
    for i in range(len(df.index)):
        similarity[i] = cosine_similarity(vect[i],vect[orig_id])[0,0]
    
    df['similarity'] = similarity
    df_new = df[df.gender == gender]
    
    df_new.reset_index(drop = True, inplace = True)
    idx = df_new.groupby(['new_cat'])['similarity'].transform(max) == df_new['similarity']
    df_new = df_new[idx][['product_id', 'name', 'new_cat', 'brand', 'price', 'retailer_name', 'retailer_url']]
    df_new = df_new.drop_duplicates(subset = ['new_cat'], keep = 'last')
    
    return df_new

def eucldist_vectorized(coords1, coords2):
    return np.sqrt(np.sum((coords1 - coords2)**2))

def OutfitGeneratorDist(product_id):
    orig_id = df.loc[df['product_id'] == product_id].index[0]
    gender = df.loc[df['product_id'] == product_id]['gender'].item()
    
    dst = [0] * len(df.index)
    #similarity = [0] * len(df.index)
    for i in range(len(df.index)):
        #similarity[i] = cosine_similarity(vect[i],vect[orig_id])[0,0]
        dst[i] = eucldist_vectorized(vect[i],vect[orig_id])
    
    
    #df['similarity'] = similarity
    df['dist'] = dst
    df_new = df[df.gender == gender]
    
    #idx = df.groupby(['new_cat'])['similarity'].transform(max) == df['similarity']
    df_new.reset_index(drop = True, inplace = True)
    idx = df_new.groupby(['new_cat'])['dist'].transform(min) == df_new['dist']
    df_new = df_new[idx][['product_id', 'name', 'new_cat', 'brand', 'price', 'retailer_name', 'retailer_url']]
    df_new = df_new.drop_duplicates(subset = ['new_cat'], keep = 'last')
    
    return df_new

#def Amz2Emd(amz_id):
##    conn = sql.connect('amazon.db')
##    cur = conn.cursor()
##    cur.execute('SELECT review_concat FROM products WHERE product_id = ?;', [amz_id])
##    res = cur.fetchall()
##    base = ''
##    for x in res:
##        base += x[0]
##    base = base.lower().split()
#    base = ''
#    for x in amz_id:
#        base += x
#    base = base.lower().split()
#    base = [w for w in base if w not in stop_words and re.match(r'[^\W\d]*$', w)]
#    
#    mind = 100
#    emd_id = 0
#    for i in range(1, 1566):
#        match = df.iloc[i]['description'].lower().split()
#        match = [w for w in match if w not in stop_words and re.match(r'[^\W\d]*$', w)]
#        d = model.wmdistance(base, match)
#        if (d < mind):
#            mind = d
#            emd_id = df.iloc[i]['product_id'] 
##    cur.close()
##    conn.close()
#    
#    return(emd_id)
