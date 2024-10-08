# -*- coding: utf-8 -*-
"""Approach1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CvjQs05IgzhGfJZZ3tQB_WI8TWi6aOZF
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics as met
from sklearn import neighbors as nei
from sklearn import decomposition as dec
from sklearn import manifold as man

df = pd.read_csv("train.csv")

df.head()

df[df["userID"]==629]

df.isnull().sum()

train = df.pivot(index="userID", columns="movieID", values="rating")
train.head()

train.shape

test = pd.read_csv("test_without_labels.csv")
test.head()

train_scaled = train - train.mean(axis=1).values.reshape(-1, 1)
train_scaled.fillna(0, inplace=True)
train_scaled.head()

testn = pd.DataFrame()
testn["userID"] = test["IDs"].str.split("_").apply(lambda x:x[0])
testn["movieID"] = test["IDs"].str.split("_").apply(lambda x:x[1])
testn.head()

testn.shape

preds = []
testusers = testn["userID"].values
#len(testusers)
for i in range(len(testusers)):
  #print(testusers[i])
  userId = int(testusers[i])
  movie = int(testn.iloc[i,1])
  #print(movie)
  k = 22
  test_user = train_scaled.loc[userId:userId, :]

  filtered_indices = train[np.isnan(train.loc[:, movie]) == False].index
  filtered_train = train_scaled.loc[filtered_indices, :]

  if len(filtered_train) > 0:
    if len(filtered_train) < k:
      k = len(filtered_train)

    nn = nei.NearestNeighbors(n_neighbors=k, metric="cosine", algorithm="brute")
    nn.fit(filtered_train)
    close_indices = nn.kneighbors(test_user, return_distance=False)[0]
    std = filtered_train.iloc[close_indices, :][movie].mean()
    avg = train.loc[userId, :].mean()
    pred = avg + std
    preds.append(pred)

preds

testnew = pd.concat([test,pd.Series(preds)],axis=1)
testnew = testnew.rename(columns={0:"rating"})
testnew.head()

testnew.to_csv("usertouserk22.csv", index=False)