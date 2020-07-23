from typing import Optional, List, Tuple, Dict
from API.body_models import UserIn, UserOut
from API.db_models import User, Post, Comment


def get_user(user_name: str):
    user = User.objects(user_name=user_name).first()
    return user


def get_user_by_email(email: str):
    user = User.objects(email=email).first()
    return user


def get_users():
    users = User.objects()
    return users


def create_user(user_in: UserIn):
    hashed_password = user_in.password
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name,
        email=user_in.email,
        password=user_in.hashed_password
    )
    user.save()
    return UserOut(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name,
        email=user_in.email
    )
