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
    posts: List = ListField(ObjectIdField)
