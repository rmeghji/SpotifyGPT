#run.py
from flask import Flask
from flask_cors import CORS
from spotify_auth import api_bp
from main import app_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
CORS(app)
app.register_blueprint(api_bp)
app.register_blueprint(app_bp)

if __name__ == '__main__':
    app.run()