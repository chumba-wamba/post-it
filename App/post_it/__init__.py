from flask import Flask, session
# from flask_session import Session
import redis

app = Flask(__name__)
app.secret_key = "secret-key"
# app.config["SESSION_TYPE"] = "redis"
# app.config["SESSION_REDIS"] = redis.from_url('redis://127.0.0.1:6379')
# sess = Session()
# sess.init_app(app=app)
redis_db = redis.Redis(host='localhost', port=6379, db=0)
api_url = "http://127.0.0.1/"

from post_it import routes