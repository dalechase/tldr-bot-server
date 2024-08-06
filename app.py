from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

CORS(app, resources={r"*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

with app.app_context():
    import routes

