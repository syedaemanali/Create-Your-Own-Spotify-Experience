from flask import Flask, jsonify
from confluent_kafka import Consumer, KafkaError
from flask import Flask, render_template
from pymongo import MongoClient
import os
import librosa
import numpy as np
import random

app = Flask(__name__)

# Initialize Kafka Consumer
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'music_topic'

conf = {'bootstrap.servers': kafka_bootstrap_servers, 'group.id': 'my_consumer_group', 'auto.offset.reset': 'earliest'}
consumer = Consumer(**conf)
consumer.subscribe([kafka_topic])

# Initialize MongoDB client
mongo_uri = 'mongodb://localhost:27017/'
mongo_db = 'bda_project'
mongo_collection = 'clusters'

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

def extract_features(song_path):
    y, sr = librosa.load(song_path)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features = np.concatenate((chroma_stft, mfcc, spectral_centroid, spectral_bandwidth, spectral_rolloff), axis=0)
    return features

def calculate_similarity(song1, song2):
    # Calculate Jaccard similarity between two sets of shingles
    intersection = len(song1.intersection(song2))
    union = len(song1.union(song2))
    return intersection / union if union != 0 else 0

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/recommended_songs', methods=['GET'])
def get_recommended_songs():
    recommended_songs = []

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                break
            else:
                print(msg.error())
                continue
        song_name = msg.value().decode('utf-8')
        song_cluster = collection.find_one({'name': song_name})['cluster']
        song_shingles = set(collection.find_one({'name': song_name})['shingles'])
        
        similar_songs = []
        for song in collection.find({'cluster': song_cluster}):
            other_song_shingles = set(song['shingles'])
            similarity = calculate_similarity(song_shingles, other_song_shingles)
            similar_songs.append((song['name'], similarity))
        
        # Sort similar songs by similarity score (descending) and get top 5
        similar_songs.sort(key=lambda x: x[1], reverse=True)
        top_5_songs = [song[0] for song in similar_songs[:5]]
        recommended_songs.extend(top_5_songs)

    return jsonify(recommended_songs)

if __name__ == '__main__':
    app.run(debug=True)
