from typing import Optional, List, Tuple, Dict
from mongoengine import Document
from mongoengine import StringField, IntField, DateTimeField, ListField, ObjectIdField
from datetime import datetime


class User(Document):
    first_name: str = StringField(required=True)
    last_name: str = StringField(required=False)
    user_name: str = StringField(required=True, unique=True)
    email: str = StringField(required=True, unique=True)
    password: str = StringField(required=True)
    posts: List = ListField(ObjectIdField())


class Post(Document):
    title: str = StringField(required=True)
    post: str = StringField(required=True)
    date_defined = DateTimeField(default=datetime.now)
    likes: int = IntField()
    liked_by: List = ListField(ObjectIdField())
    comments: List = ListField(ObjectIdField())


class Comment(Document):
    comment: str = StringField(required=True)
    date_defined = DateTimeField(default=datetime.now)
    likes: IntField()
