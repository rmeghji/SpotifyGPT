# spotify_auth.py
from flask import Flask, redirect, request, Blueprint, url_for, session, jsonify, current_app
from flask_cors import cross_origin
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from run import app

api_bp = Blueprint('api', __name__)

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
        self.spotify = spotipy.Spotify(auth=token, auth_manager=self.auth_manager)
        session['spotify_access_token'] = token
        session.modified = True
        return f"Logged in to Spotify as {self.spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat."

    @api_bp.route('/callback', methods=['POST', 'OPTIONS'])
    @cross_origin(origins=['http://localhost:5173/, https://spotifygpt.pages.dev/'], supports_credentials=True)
    def callback():
        '''New callback method that is called from frontend after user logs in to Spotify, taking in the code from the URL.'''
        code = request.get_json()['code']
        # token = self.auth_manager.get_access_token(code=code)['access_token']
        # token = SpotifyManager.get_instance().auth_manager.get_access_token(code=code)['access_token']

        # global spotify
        # spotify = spotipy.Spotify(auth=token)

        # print(f"code: {code}")

        status = SpotifyManager.get_instance().authenticate(code)
        # print(f"status: {status}")
        
        token = SpotifyManager.get_instance().auth_manager.get_access_token(code=code)['access_token']
        session['spotify_access_token'] = token
        session.modified = True

        response = jsonify({'login_status': status})
        response.headers['Access-Control-Allow-Origin'] = 'https://spotifygpt.pages.dev'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization, access-control-allow-origin, access-control-allow-methods, access-control-allow-headers, access-control-allow-credentials'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @api_bp.route('/login', methods=['GET'])
    @cross_origin(origins=['http://localhost:5173/, https://spotifygpt.pages.dev/'], supports_credentials=True)
    def login():
        '''New login method that returns jsonified url instead of redirecting.'''
        response = jsonify({'url': SpotifyManager.get_instance().auth_manager.get_authorize_url()})
        response.headers['Access-Control-Allow-Origin'] = 'https://spotifygpt.pages.dev'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization, access-control-allow-origin, access-control-allow-methods, access-control-allow-headers, access-control-allow-credentials'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response