from flask import Flask
from flask_session import Session
import redis

app = Flask(__name__)
# app.config["SESSION_TYPE"] = "redis"
# app.config["SESSION_REDIS"] = redis.from_url("127.0.0.1:6379")
session = Session()
session.init_app(app=app)

from post_it import routes