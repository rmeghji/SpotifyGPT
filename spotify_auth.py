# spotify_auth.py
from flask import Flask, redirect, request, Blueprint, url_for, session, jsonify, current_app, make_response
from flask_cors import cross_origin, CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth

api_bp = Blueprint('api', __name__)
CORS(api_bp,
    supports_credentials=True,
    allow_headers=['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-headers', 'access-control-allow-credentials', 'Authorization'],
    origins=['http://localhost:5173/', 'https://spotifygpt.pages.dev'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    )

scope = ['user-read-playback-state', 'user-modify-playback-state', 'user-library-read', 'user-follow-read', 'playlist-read-private', 'user-read-recently-played']

class SpotifyManager:
    _instance = None

    def __init__(self) -> None:
        self.cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
        self.scope = ['user-read-playback-state', 'user-modify-playback-state', 'user-library-read', 'user-follow-read', 'playlist-read-private', 'user-read-recently-played']
        self.auth_manager = SpotifyOAuth(scope=self.scope, open_browser=False, cache_handler=self.cache_handler)
        self.spotify = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def authenticate(self, code):
        token = self.auth_manager.get_access_token(code=code)['access_token']
        self.spotify = spotipy.Spotify(auth=token, auth_manager=self.auth_manager)
        # session['spotify_access_token'] = token
        # session.modified = True
        return f"Logged in to Spotify as {self.spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat."
    
    # @api_bp.before_app_request
    # def before_request():
    #     if 'spotify_access_token' not in session:
    #         session['spotify_access_token'] = None

    @api_bp.route('/callback', methods=['POST', 'OPTIONS'])
    @cross_origin(supports_credentials=True)
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
        
        # token = SpotifyManager.get_instance().auth_manager.get_access_token(code=code)['access_token']
        # token = SpotifyOAuth(scope=scope).get_access_token(code=code)['access_token']

        # session['spotify_access_token'] = token
        # session.modified = True

        print(f"token immediately after auth: {session.get('spotify_access_token')}")
        print(f"cookie domain in callback: {current_app.config['SESSION_COOKIE_DOMAIN']}")
        print(f"cookies in callback req: {request.cookies}")

        response = make_response(jsonify({'login_status': "valid"}), 200)
        # response.set_cookie('spotify_access_token', token, samesite="None", httponly=True, secure=True)

        return response

    @api_bp.route('/login', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def login():
        '''New login method that returns jsonified url instead of redirecting.'''
        session.clear()
        session.modified = True
        response = make_response(jsonify({'url': SpotifyManager.get_instance().auth_manager.get_authorize_url()}), 200)
        return response
    
    @api_bp.route('/test', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def test():
        response = make_response(jsonify({'api_key': session.get('spotify_access_token')}), 200)
        session['test'] = 'test'
        return response