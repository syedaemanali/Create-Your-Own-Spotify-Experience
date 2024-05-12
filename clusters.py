#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import librosa
import numpy as np
import random
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import io
import csv
from pymongo import MongoClient


# In[ ]:


df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()


# In[ ]:


genres = df['Genres']
Tracks = df['Track ID'].tolist()
#tracks = df.index.tolist()
# Initialize list to store extracted genre IDs
GenreIDs = []

# Iterate over each string in the list
for string in genres:
    # Convert to string if it's not already
    string = str(string)
    
    # Find the index of the substring 'genre_id'
    index_start = string.find("'genre_id': '") + len("'genre_id': '")
    index_end = string.find("'", index_start)
    
    # Extract the number
    genre_id = string[index_start:index_end]
    GenreIDs.append(genre_id)

GenreID = {}

for i in range(len(Tracks)):
    GenreID[Tracks[i]] = GenreIDs[i]

    
print(GenreID)


# In[ ]:


AlbumID = df['Album ID'].tolist()

albumID = {}

for i in range(len(tracks)):
    albumID[Tracks[i]] = AlbumID[i]

print(albumID)


# In[ ]:


ArtistID = df['Artist ID'].tolist()

artistID = {}

for i in range(len(tracks)):
    albumID[Tracks[i]] = ArtistID[i]

print(albumID)


# In[ ]:


# Create a dictionary with column names and lists
data = {
    'Track ID': Tracks,
    'Genre': GenreIDs,
    'Artist': ArtistID,
    'Album': AlbumID
}

# Create a DataFrame from the dictionary
k_means = pd.DataFrame(data)


# In[ ]:


k_means.columns = k_means.columns.astype(str)

# Encode categorical variables
label_encoder = LabelEncoder()

# Iterate over each column and encode non-numeric values
for column in k_means.columns:
    if k_means[column].dtype == object:
        k_means[column] = label_encoder.fit_transform(k_means[column])

# Handle missing values
imputer = SimpleImputer(strategy='mean')
k_means_imputed = pd.DataFrame(imputer.fit_transform(k_means), columns=k_means.columns)

# Perform k-means clustering
k = 20  # You can change the number of clusters as needed
kmeans = KMeans(n_clusters=k)
kmeans.fit(k_means_imputed)

# Add cluster labels to the dataframe
k_means_imputed['Cluster'] = kmeans.labels_

# Print the resulting dataframe
print(k_means_imputed)


# In[ ]:


# Create a dictionary with column names and lists
data = {
    'Track ID': Tracks,
    'Cluster': k_means_imputed['Cluster']
}

# Create a DataFrame from the dictionary
clusters = pd.DataFrame(data)


# In[ ]:


# MongoDB connection
client = MongoClient('localhost', 27017)  # Assuming MongoDB is running locally
db = client['bda_project']
collection = db['clusters']


# In[ ]:


records = df.to_dict(orient='records')

# Insert records into MongoDB
collection.insert_many(records)

# Close MongoDB connection
client.close()

