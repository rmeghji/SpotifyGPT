from flask import Flask, redirect, request
from flask_cors import cross_origin
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .import app

class SpotifyManager:
    _instance = None

    def __init__(self) -> None:
        self.scope = ['user-read-playback-state', 'user-modify-playback-state', 'user-library-read', 'user-follow-read', 'playlist-read-private', 'user-read-recently-played']
        self.auth_manager = SpotifyOAuth(scope=self.scope, open_browser=False)
        self.spotify = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def authenticate(self, code):
        token = self.auth_manager.get_access_token(code=code)['access_token']
        self.spotify = spotipy.Spotify(auth=token)
        return f"Logged in to Spotify as {self.spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat."
    
    @app.route('/callback', methods=['GET'])
    @cross_origin(origins=['http://localhost:5173'])
    def callback(self):
        code = request.args['code']
        token = self.auth_manager.get_access_token(code=code)['access_token']
        global spotify
        spotify = spotipy.Spotify(auth=token)
        print(f"Logged in to Spotify as {spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat.")

        response = redirect('http://localhost:5173/')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization, access-control-allow-origin, access-control-allow-methods, access-control-allow-headers'
        return response

    @app.route('/login', methods=['GET'])
    @cross_origin(origins=['http://localhost:5173'])
    def login():
        response = redirect(self.auth_manager.get_authorize_url())
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response