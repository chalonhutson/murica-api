from os import environ
from flask import Flask, render_template, url_for, jsonify, request, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

from .model import db, connect_to_db, User, APIKey, APIRequest, Character

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ["POSTGRES_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_to_db(app)
migrate = Migrate(app, db)
CORS(app)

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")