#run.py
from flask import Flask, session, render_template
from flask_cors import CORS
from spotify_auth import api_bp
from main import app_bp
import os
from flask_session import Session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
CORS(app)
app.register_blueprint(api_bp)
app.register_blueprint(app_bp)
Session(app)

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

if __name__ == '__main__':
    app.run()