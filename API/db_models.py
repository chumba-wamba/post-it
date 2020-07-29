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


class Post(Document):
    author: str = StringField()
    title: str = StringField(required=True)
    body: str = StringField(required=True)
    date_defined = DateTimeField(default=datetime.now)
    likes: int = IntField()
    liked_by: List = ListField(ObjectIdField())


class Comment(Document):
    author: str = StringField()
    post_id: str = ObjectIdField()
    comment: str = StringField(required=True)
    date_defined = DateTimeField(default=datetime.now)
    likes: int = IntField()
    liked_by: List = ListField(ObjectIdField())
