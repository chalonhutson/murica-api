from flask_sqlalchemy import SQLAlchemy
from random import choice
from string import ascii_letters, digits

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(99), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    api_tokens = db.relationship("User", lazy="select", backref=db.backref("user", lazy="joined"))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User id:{self.id} username:{self.username}>"


class APIToken(db.Model):

    __tablename__ = "api_tokens"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    api_token = db.Column(db.String(99), nullable=False, unique=True)

    def __init__(self, user_id):
        self.user_id = user_id
        self.api_token = generate_api_key()

    def __repr__(self):
        return f"<API Token user_id:{self.user_id}>"

    def get_current_tokens():
        return [x.api_toke for x in APIToken.query.all()]

    def generate_api_key():
        api_key = []

        while len(api_key) < 40:
            api_key.append(choice(ascii_letters + digits))

            api_key = "".join(api_key)

        if api_key in get_current_tokens():
            generate_api_key()
        else:   
            return api_key


def connect_to_db(app):
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from os import environ
    from flask import Flask
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    connect_to_db(app)
    print("Connected to the database...")



