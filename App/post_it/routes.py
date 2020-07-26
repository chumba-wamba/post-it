from flask import render_template, url_for, jsonify, request
from requests import get, post
from functools import wraps
from post_it import app, redis_db, api_url
from post_it.forms import *


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def root():
    return {"message": "welcome to the post-it client"}


@app.route("/register")
def register():
    pass


@app.route("/login")
def login():
    pass


@app.route("/home")
def home():
    pass
