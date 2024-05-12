# Create-Your-Own-Spotify-Experience

i221936 i221871 i221953 

BDA Semester End Project

Phase I:
Pre-processing audio data: 
Enhanching audio quality
Compressing audio files
Checked for distortion
Equaised Audio

Phase II :

Performing Feature Extraction:
Used the Librosa library to form numerical vectors of our audio files.

Performing LSH:
Created shingles from numerical audio vectors and performed jaccard similarity on them.

Performing K-Means Clustering:
Performed K-Means clustering on Genre, Artist and Album from Tracks csv. To cluster similar songs together.

How it all works together:
K-Means clustering is performed on all the songs and all song track ids are stored in mongo db with their cluster numbers. Once the user shows interest in a song, all other songs from that share the same cluster are pulled out and lsh is performed. We calculate Jaccard similarity between all these songs and the song the user streamed, then select the top 5 with the highest similarity, to be displayed on the web page as recommendations

Phase III:
Sure, here's a simple breakdown of how your Flask application with Kafka Consumer works:

- Flask Application:
  - Renders HTML templates using `render_template` or returns JSON responses using `jsonify`.

- **Kafka Consumer**:
  - It subscribes to a Kafka topic (`music_topic`) where messages (song names) are published.
  - Polls the Kafka topic to receive messages.
  - Decodes the received messages to extract song names.
  - Queries MongoDB to retrieve additional information about the songs (e.g., cluster, shingles).
  - Calculates similarity between songs based on their shingles.
  - Returns the top 5 recommended songs as a JSON response.

- **MongoDB**:
  - Stores data about each song, including its name, cluster, and shingles.

- **Feature Extraction** (Librosa and NumPy):
  - Uses Librosa library to extract audio features from songs (e.g., chroma, MFCC).
  - Combines extracted features into a feature vector using NumPy.

- **Similarity Calculation**:
  - Uses Jaccard similarity to measure similarity between sets of shingles.
  - Compares the shingles of the current song with other songs in the same cluster.
  - Ranks songs based on their similarity scores and selects the top 5 similar songs.

- **Web Interface**:
  - Provides a simple web interface with an index page (`/`) and a recommended songs page (`/recommended_songs`).
  - The index page welcomes users and provides a link to the recommended songs page.
  - The recommended songs page displays the top 5 recommended songs based on user interactions with the web application.

This setup allows users to receive personalized music recommendations based on the songs they interact with in real-time through the web interface.

