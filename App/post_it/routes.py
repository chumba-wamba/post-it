from flask import render_template, url_for, jsonify, session
from requests import get, post
from functools import wraps
from post_it import app, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def root():
    return {"message": "hello, world"}
