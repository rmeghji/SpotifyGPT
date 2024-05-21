# spotify_tools.py
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from langchain.agents import tool
from flask import Flask, redirect, session
from spotify_auth import SpotifyManager
# from main import spotify
# from flask_cors import CORS, cross_origin
# from main import app

# OAUTH_ARGS = {'client_id': SPOTIPY_CLIENT_ID, 'client_secret': SPOTIPY_CLIENT_SECRET, 'redirect_uri': SPOTIPY_REDIRECT_URI, 'scope': scope}
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

# spotify = SpotifyManager.get_instance().spotify

def with_spotify_auth(func):
    @tool
    def wrapper(*args, **kwargs):
        '''Wrapper function that checks if the user is logged into Spotify and has the necessary permissions. If so, it runs the function. If not, it tells the user to log in to Spotify and grant the necessary permissions.'''
        if not session['spotify_access_token']:
            return "Please log in to Spotify first.\n"
        else:
            spotify = spotipy.Spotify(auth=session['spotify_access_token'])
        return func(spotify, *args, **kwargs)
    return wrapper


@with_spotify_auth
def check_login(spotify):
    '''Checks that the user is logged into Spotify and has the necessary permissions. If not, tells the user to log in to Spotify and grant the necessary permissions, providing a URL to do so which should be given to the user.'''
    while True:
        try:
            # spotify = SpotifyManager.get_instance().spotify
            # global spotify
            # spotify = spotipy.Spotify(auth=session['spotify_access_token'])
            spotify.current_user()
            break
        except:
            # spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
            return f"User is not logged into Spotify or does not have the necessary permissions. Please log in to Spotify and grant the necessary permissions.\n"
            # auth_manager._get_auth_response_interactive(open_browser=True)
            spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth())

    return "User is logged into Spotify and has the necessary permissions.\n"

@with_spotify_auth
def current_track(spotify):
    '''Returns the current track playing on the user's Spotify account in the format "Artist Name - Song Title".'''
    return f"{spotify.current_playback()['item']['artists'][0]['name']} - {spotify.current_playback()['item']['name']}\n"

@with_spotify_auth
def skip(spotify):
    '''Skips to the next track in the user's Spotify queue. Tells user what song is now playing.'''
    spotify.next_track()
    sleep(0.5)
    return f"Skipped to the next track. Now playing is {spotify.current_playback()['item']['artists'][0]['name']} - {spotify.current_playback()['item']['name']}.\n"

@with_spotify_auth
def pause(spotify):
    '''Pauses the current track in the user's Spotify queue.'''
    if spotify.current_playback()['is_playing']:
        spotify.pause_playback()
        return f"Paused the current track.\n"
    else:
        return f"Playback is already paused.\n"

@with_spotify_auth
def play(spotify):
    '''Plays the current track in the user's Spotify queue.'''
    if not spotify.current_playback()['is_playing']:
        spotify.start_playback()
        return f"Playing the current track.\n"
    else:
        return f"The current track is already playing.\n"
    
@with_spotify_auth
def search(spotify, input: str):
    '''Takes in a user's request and finds songs, albums, artists, or playlists that match the query.'''
    results = spotify.search(q=input, limit=2, type='track,album,artist,playlist')
    songs = '\n'.join([f"{result['name']} by {result['artists'][0]['name']}\nURI: {result['uri']}" for result in results['tracks']['items']])
    albums = '\n'.join([f"{result['name']} by {result['artists'][0]['name']}\nURI: {result['uri']}" for result in results['albums']['items']])
    artists = '\n'.join([f"{result['name']}\nURI: {result['uri']}" for result in results['artists']['items']])
    playlists = '\n'.join([f"{result['name']} by {result['owner']['display_name']}\nURI: {result['uri']}" for result in results['playlists']['items']])

    return f"Search results for '{input}':\nSongs:\n{songs}\n\nAlbums:\n{albums}\n\nArtists:\n{artists}\n\nPlaylists:\n{playlists}\n"

@with_spotify_auth
def narrow_search(spotify, song_uris: list, album_uris: list, artist_uris: list, playlist_uris: list):
    '''Takes in all URI values from the results of a search query and narrows down the search to items that are saved in the user's Spotify account or artists that the user follows.'''
    track_uris = song_uris
    saved_tracks = []
    if song_uris:
        saved_tracks_uris = spotify.current_user_saved_tracks_contains(tracks=track_uris)
        saved_tracks = [uri for i, uri in enumerate(track_uris) if saved_tracks_uris[i]]
        saved_tracks = [f"{spotify.track(track_id=track_uri)['artists'][0]['name']} - {spotify.track(track_id=track_uri)['name']}" for track_uri in saved_tracks]

    saved_albums = []
    if album_uris:
        saved_albums_uris = spotify.current_user_saved_albums_contains(albums=album_uris)
        saved_albums = [uri for i, uri in enumerate(album_uris) if saved_albums_uris[i]]
        saved_albums = [f"{spotify.album(album_id=album_uri)['artists'][0]['name']} - {spotify.album(album_id=album_uri)['name']}" for album_uri in saved_albums]
    
    followed_artists = []
    if artist_uris:
        followed_artists_uris = spotify.current_user_following_artists(ids=artist_uris)
        followed_artists = [uri for i, uri in enumerate(artist_uris) if followed_artists_uris[i]]
        followed_artists = [spotify.artist(artist_id=artist_uri)['name'] for artist_uri in followed_artists]

    my_playlists = []
    user_playlists = spotify.current_user_playlists()
    if playlist_uris:
        my_playlists = [uri for i, uri in enumerate(playlist_uris) if spotify.playlist(playlist_id=uri.split(':')[-1]) in user_playlists['items']]
        my_playlists = [spotify.playlist(playlist_id=playlist_uri.split(':')[-1])['name'] for playlist_uri in my_playlists]

    return f"Saved tracks:\n{saved_tracks}\n\nSaved albums:\n{saved_albums}\n\nFollowed artists:\n{followed_artists}\n\nFollowed playlists:\n{my_playlists}\n"

# @tool
# def narrow_search(track_uris: list):
#     '''Takes in all song URI values from the results of a search query and narrows down the search to tracks that are saved in the user's Spotify account.'''
#     saved_tracks_uris = spotify.current_user_saved_tracks_contains(tracks=track_uris)
#     return saved_tracks_uris
#     # saved_albums_uris = spotify.current_user_saved_albums_contains(albums=album_uris)
#     # followed_artists_uris = spotify.current_user_following_artists(ids=artist_uris)
#     # followed_playlists_uris = [spotify.playlist_is_following(playlist_id=playlist_uri.split(':')[-1], user_ids=[spotify.current_user()['id']]) for playlist_uri in playlist_uris]

#     saved_tracks = [f"{spotify.track(track_id=track_uri)['artists'][0]['name']} - {spotify.track(track_id=track_uri)['name']}" for track_uri in saved_tracks_uris]
#     # saved_albums = [f"{spotify.album(album_id=album_uri)['artists'][0]['name']} - {spotify.album(album_id=album_uri)['name']}" for album_uri in saved_albums_uris]
#     # followed_artists = [spotify.artist(artist_id=artist_uri)['name'] for artist_uri in followed_artists_uris]
#     # followed_playlists = [spotify.playlist(playlist_id=playlist_uri)['name'] for playlist_uri in followed_playlists_uris]

#     return f"Saved tracks:\n{saved_tracks}"
#     # \n\nSaved albums:\n{saved_albums}\n\nFollowed artists:\n{followed_artists}\n\nFollowed playlists:\n{followed_playlists}\n"

# @tool
# def play_song(song_name: str):
#     '''Finds and plays a song with the given name on the user's Spotify account.'''
#     spotify.start_playback(uris=[spotify.search(q=song_name, limit=1, type='track')['tracks']['items'][0]['uri']])
#     return f"Playing {song_name}.\n"

@with_spotify_auth
def play_song(spotify, song_uri: str):
    '''Plays a song with the given URI on the user's Spotify account.'''
    spotify.start_playback(uris=[song_uri])
    return f"Playing song.\n"

# @tool
# def play_album(album_name: str):
#     '''Finds and plays an album with the given name on the user's Spotify account.'''
#     spotify.start_playback(context_uri=spotify.search(q=album_name, limit=1, type='album')['albums']['items'][0]['uri'])
#     return f"Playing {album_name}.\n"

@with_spotify_auth
def play_album(spotify, album_uri: str):
    '''Plays an album with the given URI on the user's Spotify account.'''
    spotify.start_playback(context_uri=album_uri)
    return f"Playing album.\n"

# @tool
# def play_artist(artist_name: str):
#     '''Finds and plays an artist with the given name on the user's Spotify account.'''
#     artist_id = spotify.search(q=artist_name, limit=1, type='artist')['artists']['items'][0]['id']
#     spotify.start_playback(context_uri=f"spotify:artist:{artist_id}")
#     return f"Playing {artist_name}.\n"

@with_spotify_auth
def play_artist(spotify, artist_uri: str):
    '''Plays an artist with the given URI on the user's Spotify account.'''
    spotify.start_playback(context_uri=artist_uri)
    return f"Playing artist.\n"

# @tool
# def play_playlist(playlist_name: str):
#     '''Finds and plays a playlist with the given name on the user's Spotify account.'''
#     playlist_id = spotify.search(q=playlist_name, limit=1, type='playlist')['playlists']['items'][0]['id']
#     spotify.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
#     return f"Playing {playlist_name}.\n"

# @with_spotify_auth
# def play_playlist(spotify, playlist_uri: str):
#     '''Plays a playlist with the given URI on the user's Spotify account.'''
#     spotify.start_playback(context_uri=playlist_uri)
#     return f"Playing playlist.\n"

@with_spotify_auth
def queue_song(spotify, song_name: str):
    '''Queues a song with the given name to the user's Spotify queue.'''
    spotify.add_to_queue(song_name)
    return f"Queued {song_name}.\n"