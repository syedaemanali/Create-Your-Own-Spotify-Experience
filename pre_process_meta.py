import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv(r"D:\track_metadata.csv\fma_metadata\raw_tracks.csv")  # Assuming the header is in the second row
print(df)
print("Shape of df before removing any columns or null rows",df.shape)
columns_to_keep = ['track_id', 'album_id', 'album_title', 'artist_id', 'artist_name', 'track_bit_rate', 'track_composer', 'track_date_created', 'track_date_recorded', 'track_disc_number', 'track_duration', 'track_genres', 'track_lyricist', 'track_number', 'track_title']
df = df[columns_to_keep]


print(df)
print(df.columns)

# Count rows that are completely null
null_rows_count = df.isnull().all(axis=1).sum()
print("Count of rows that are completely null:", null_rows_count)
# Remove rows that are completely null
df = df.dropna(how='all')

print("Shape of df after removing any columns or null rows",df.shape)


# Change date columns to date type
date_columns = ['track_date_created', 'track_date_recorded']
for col in date_columns:
    df[col] = pd.to_datetime(df[col])

print(df.columns)
 #Rename columns to meaningful names
column_mapping = {
    'track_id': 'Track ID',
    'album_id': 'Album ID',
    'album_title': 'Album Title',
    'artist_id': 'Artist ID',
    'artist_name': 'Artist Name',
    'track_bit_rate': 'Bit Rate',
    'track_composer': 'Composer',
    'track_date_created': 'Date Created',
   'track_date_recorded': 'Date Recorded',
   'track_duration': 'Duration',
  'track_genres': 'Genres',
    'track_lyricist': 'Lyricist',
    'track_number': 'Track Number',
   'track_title': 'Track Title'
}
df = df.rename(columns=column_mapping)

print(df)

# Save the preprocessed DataFrame to a CSV file
df.to_csv("pre-processed_metadata.csv", index=False)
