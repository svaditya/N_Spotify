import os
import pandas as pd
import subprocess as sp
import json
import re
import ast

def string_fix(x):
    x = ast.literal_eval(x)
    #print(type(x))
    return x 
    
user = 'vkrolsnfcgkhtnmh5hz83ndh6'
output = sp.getoutput('python3 examples/user_public_playlists.py ' + user)

playlists= []
for i in output.split('\n'):
    playlists.append((i.lstrip().rstrip().split(' '))[1])

result = []
for playlist in playlists:
    print('Playlist:' + playlist)
    output = sp.getoutput('python3 examples/playlist_tracks.py ' + playlist)
    tracks = re.findall(r"'id': '(.*)'", output)
    for track in tracks:
        #print('Track: ' + track)
        to = sp.getoutput('python3 examples/show_track_info.py ' + track)
        artists = string_fix(to)['artists'] 
        artist_info = []
        for artist in artists:
            artist_info.append((artist['id'], artist['name']))
        for artist in artist_info:
            #print('Artist: ' + artist[0] + artist[1])
            # Similarity is based on analysis of the Spotify community’s listening
            related_artists = sp.getoutput('python3 examples/show_related.py ' + artist[1])
            related_artists = [i.lstrip().rstrip() for i in related_artists.split('\n')]
            for related_artist in related_artists:
                #print('Related Artist: ' + related_artist)
                artist_top_tracks = sp.getoutput('python3 examples/show_artist_top_tracks.py spotify:artist:' + related_artist)
                artist_top_tracks = string_fix(artist_top_tracks)
                for top_track in artist_top_tracks:
                    #print('Related Artist Top Track: ' + top_track['name'])
                    res = (playlist, track, artist[0], artist[1], related_artist, top_track['name'], top_track['id'])
                    result.append(res)
                    #break
                #break
            #break
        #break
    #break

df = pd.DataFrame(result, columns =['OriginalPlaylist', 'Track', 'ArtistID', 'Artistname', 'RelatedArtistName', 'RelatedArtistTopTrackName', 'RelatedArtistTrackID']) 
df.to_csv('./extended_corpus.csv')