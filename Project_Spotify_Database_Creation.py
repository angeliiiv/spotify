# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 18:42:10 2022

@author: angel
"""

"""
This part of the code below is for the Spotify API warpper Spotipy
"""
client_id = "41abbf0487be43c5876d2eb6f43c08a8"
client_secret = "87dbb59047254d959b2491e31b5d08fa"
import pandas as pd

import os
os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)



"""
This next section is to pull all the data I need for the music database
"""
# For loop that pulls everything I need for the music database
artists = ['Billie Eilish','Kendrick Lamar','Post Malone','iKON','George Strait','Justin Bieber','BTS','Drake','Doja Cat']

num_of_albums = [1,2,3,4]

df_album_final = pd.DataFrame()

for q in range(0,len(artists)): #for artists
    #finding artist ids
    artist = artists[q]
    results = sp.search(q='artist: ' + artist, type='artist')
    items = results['artists']['items']
    id_i = items[0]['external_urls']['spotify'].split('/')[-1]

    #Get album IDS
    for i in num_of_albums:    
        album_id = sp.artist_albums(id_i)['items'][i]['id']
        album_name = sp.artist_albums(id_i)['items'][i]['name']
    
        #Pulling albums
        album_tracks = sp.album_tracks(album_id)
        album_track_info = album_tracks['items']        
        album_num_tracks = len(album_track_info)
        
        for j in range(0,album_num_tracks):   
            #for the song
            album_track_id = album_track_info[j]['id']
            album_track_name = album_track_info[j]['name']
            album_track_features = sp.audio_features(album_track_id)[0]
        
            #add track info
            album_track_features['song_name'] = album_track_name
            album_track_features['artist'] = artist
            album_track_features['artist_id'] = id_i
            album_track_features['album_name'] = album_name
        
            #Make a row for data frame
            album_row = pd.DataFrame(album_track_features, index=[0])
            df_album_final = df_album_final.append(album_row)
    
            #create database
            df_album_finale = df_album_final[['artist','artist_id','album_name','song_name','danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                                         'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo','duration_ms','id']]
            
            
"""
Time to clean the data, since some of the albums are deluxe version or top 75 type albyms I want to drop any duplicate song name. 
Someof the songs have a hash with extra info or trailing spaces that make the same song appear as different to python
"""
#Checking for NaN Values
count_nan_in_df = df_album_finale.isnull().sum().sum()
print ('Count of NaN: ' + str(count_nan_in_df))
           
# Some songs are the same but have a dash. I'm splitting the dash to then drop duplicates       
df_album_finale['song_name'] = df_album_finale['song_name'].str.split('-',expand = True)

# Removing trailing spaces     
df_album_finale['song_name'] = df_album_finale['song_name'].str.rstrip()    
   
# Dropping duplicates. Focused on the song_name column        
df_album_finale2 = df_album_finale.drop_duplicates(['song_name']) 

#Checking for NaN Values
count_nan_in_df = df_album_finale2.isnull().sum().sum()
print ('Count of NaN: ' + str(count_nan_in_df)) 

# Output to CSV       
df_album_finale2.to_csv('music_database_clean.csv')




"""
While I am here I want to create a seperate database with the arrtist data. Honestly this isn't for the model I just want to do it
"""
            
# Creating a Second database with artist 'name', 'id', 'popularity', 'followers'        
df_artist_info = pd.DataFrame()

artist_name = []
artist_id = []
popularity = []
followers = []

for artist in artists:
    #Getting artist info
    results = sp.search(q='artist: ' + artist, type='artist')
    items = results['artists']['items']
    id_i2 = items[0]['id']
    popularity2 = items[0]['popularity']
    followers2 = items[0]['followers']['total']   
    
    #Append to empty lists 
    artist_name.append(artist)
    artist_id.append(id_i2)
    popularity.append(popularity2)    
    followers.append(followers2)

#Create Database  
df_artist_info['artist'] = artist_name
df_artist_info['artist_id'] = artist_id
df_artist_info['popularity'] = popularity
df_artist_info['followers'] = followers     

df_artist_info.to_csv('artist_database.csv')
    