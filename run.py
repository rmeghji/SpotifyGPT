#run.py
from flask import Flask
from flask_cors import CORS
from spotify_auth import api_bp
from main import app_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.register_blueprint(api_bp)
app.register_blueprint(app_bp)
CORS(app,
     supports_credentials=True,
     origins=['http://localhost:5173/', 'https://spotifygpt.pages.dev/'],
     allow_headers=['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-headers', 'access-control-allow-credentials'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
     )

if __name__ == '__main__':
    app.run()