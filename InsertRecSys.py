# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:30:15 2020

@author: Ankit
"""

from pymongo import MongoClient 
import pandas as pd
import sys
import numpy as np

from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
from surprise import KNNBasic

import datetime

# import ssl


class InsertRecSys:
    
    def read(self):
        today = datetime.datetime.today()
        dlower = today - datetime.timedelta(days=150)

        conn = MongoClient('192.168.1.72', 27017 ) 
        mydb = conn.SK
        collection1 = mydb.OrderMaster
        df1 = pd.DataFrame(list(collection1.find({"OrderDate":{'$lt': today, '$gte': dlower}},{"Skcode":1,"orderDetails":1,"_id":0},no_cursor_timeout=True)))
        return df1
    
    def ExtractItemid(self,df1):
        df1["item"] = [[i[j]['ItemId'] for j in range(len(i))] for i in df1['orderDetails']]
        df1 = df1[['Skcode','item']]
        df2 = df1.explode('item')
        return df2
        
    def Clean(self,df):
        df1 = df.drop_duplicates()
        df2 = df1.dropna()
        return df2
        
    def AddRating (self,df):
        df['rating'] = df.apply(lambda _: '1', axis=1)
        df['rating'] = df['rating'].astype(int)
        return df

    def RenameColumns(self,df):
        df.columns = ['userID','itemID', 'rating']
        return df
        
    def CalculateFrequency(self,df):
        a=df.groupby('itemID')['rating'].apply(list)
        b = a.to_frame()
        c = b.copy()
        c['frequency']  = [sum(i) for i in c['rating']]
        c1 = c.reset_index()
        c1
      
    
    def CalculateFrequency1(self):
        today = datetime.datetime.today()
        dlower = today - datetime.timedelta(days=30)

        conn = MongoClient('192.168.1.72', 27017)
        mydb = conn.SK
        collection1 = mydb.OrderMaster
        df = pd.DataFrame(list(collection1.find({"OrderDate":{'$lt': today, '$gte': dlower}},{"Skcode":1,"WarehouseId":1,"orderDetails":1,"OrderDate":1})))

        extractdf = InsertRecSys().ExtractItemid(df)
        extractdf['rating'] = extractdf.apply(lambda _: '1', axis=1)
        extractdf['rating'] = extractdf['rating'].astype(int)

        a=extractdf.groupby('item')['rating'].apply(list)
        b = a.to_frame()
        c = b.copy()
        c['frequency']  = [sum(i) for i in c['rating']]
        c1 = c.reset_index()
        freq_dict = {}
        litemid = list(c1['item'])
        lfrequency = list(c1['frequency'])
        freqdict = dict(zip(litemid,lfrequency))
        return freqdict
    

    def CosineSimilarityMatrix(self,df):
        temp = []
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
        k = 10
        trainSet = data.build_full_trainset()
        sim_options = {'name': 'cosine',
                       'user_based': False
                       }
        model = KNNBasic(sim_options=sim_options)
        model.fit(trainSet)
        simsMatrix = model.compute_similarities()
        lc = list(trainSet._raw2inner_id_items)
        #df = pd.DataFrame(simsMatrix , columns = lc, index = lc)     
        ltuple = (simsMatrix,lc)
        return ltuple

    def finalfreq(self,ltup):
        lfreqfinal = {}
        lfreq = InsertRecSys().CalculateFrequency1()
        ke = list(lfreq.keys())
        for i in ltup[1]:
            if (i in ke):
                lfreqfinal[i]=lfreq[i]
            else:
                lfreqfinal[i] = 1
        return lfreqfinal
    
    def insertdata(self,df):
        data_dict = df.to_dict('records')
        
        conn = MongoClient('192.168.1.101', 27017) 
        mydb = conn.ML
        collection = mydb.RecSysItem
        collection.remove() 
        collection.insert_many(data_dict)
























