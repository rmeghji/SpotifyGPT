#run.py
from flask import Flask, session
from flask_cors import CORS
from spotify_auth import api_bp
from main import app_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
# app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_COOKIE_DOMAIN'] = 'https://spotifygpt.pages.dev/chat'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.register_blueprint(api_bp)
app.register_blueprint(app_bp)
CORS(app,
     allow_headers=['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Credentials', 'Access-Control-Expose-Headers'],
     origins=['http://localhost:5173/', 'https://spotifygpt.pages.dev'],
     supports_credentials=True,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     )

if __name__ == '__main__':
    app.run()