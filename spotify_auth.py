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
    
    # @app.route('/callback', methods=['GET'])
    # @api_bp.route('/callback', methods=['GET'])
    # @cross_origin(origins=['http://localhost:5173, https://accounts.spotify.com/authorize'])
    # def callback():
    #     code = request.args['code']
    #     # token = self.auth_manager.get_access_token(code=code)['access_token']
    #     # token = SpotifyManager.get_instance().auth_manager.get_access_token(code=code)['access_token']

    #     # global spotify
    #     # spotify = spotipy.Spotify(auth=token)

    #     print(SpotifyManager.get_instance().authenticate(code))

    #     # print(f"Logged in to Spotify as {spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat.")

    #     # session['spotify_access_token'] = token

    #     response = redirect('http://localhost:5173')
    #     # response = redirect()
    #     # response = redirect(url_for('app'))
    #     # response = redirect(url_for('app.chat'))
    #     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173, https://accounts.spotify.com/authorize'
    #     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    #     response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization, access-control-allow-origin, access-control-allow-methods, access-control-allow-headers'
    #     response.headers['Access-Control-Allow-Credentials'] = 'true'
    #     return response

    @api_bp.route('/callback', methods=['POST'])
    # @cross_origin()
    def callback():
        '''New callback method that is called from frontend after user logs in to Spotify, taking in the code from the URL.'''
        # code = request.args['code']
        # code = request.form['code']
        code = request.get_json()['code']
        # token = self.auth_manager.get_access_token(code=code)['access_token']
        # token = SpotifyManager.get_instance().auth_manager.get_access_token(code=code)['access_token']

        # global spotify
        # spotify = spotipy.Spotify(auth=token)

        print(f"code: {code}")

        status = SpotifyManager.get_instance().authenticate(code)
        print(f"status: {status}")
        return jsonify({'login_status': status})

        # # print(f"Logged in to Spotify as {spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat.")

        # # session['spotify_access_token'] = token

        # # response = redirect('http://localhost:5173')
        # # response = redirect()
        # # response = redirect(url_for('app'))
        # # response = redirect(url_for('app.chat'))
        # # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173, https://accounts.spotify.com/authorize'
        # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173/callback'
        # response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        # response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization, access-control-allow-origin, access-control-allow-methods, access-control-allow-headers'
        # response.headers['Access-Control-Allow-Credentials'] = 'true'
        # return response

    # @app.route('/login', methods=['GET'])
    # @api_bp.route('/login', methods=['GET'])
    # @cross_origin(origins=['http://localhost:5173/'], supports_credentials=True)
    # def login():
    #     # response = redirect(self.auth_manager.get_authorize_url())
    #     response = redirect(SpotifyManager.get_instance().auth_manager.get_authorize_url())
    #     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    #     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    #     response.headers['Access-Control-Allow-Headers'] = '*'
    #     response.headers['Access-Control-Allow-Credentials'] = 'true'
    #     return response

    @api_bp.route('/login', methods=['GET'])
    @cross_origin(origins=['http://localhost:5173/, https://rmeghji.github.io'])
    def login():
        '''New login method that returns jsonified url instead of redirecting.'''
        response = jsonify({'url': SpotifyManager.get_instance().auth_manager.get_authorize_url()})
        response.headers['Access-Control-Allow-Origin'] = 'https://rmeghji.github.io'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization, access-control-allow-origin, access-control-allow-methods, access-control-allow-headers'
        return response