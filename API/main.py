from fastapi import FastAPI, Path, Query, Body, Depends
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from mongoengine import connect
import bcrypt
from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field
from body_models import UserIn, UserOut, PostIn, PostOut, CommentIn, CommentOut
from db_models import User, Post, Comment
import db_utils


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.29/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.29/swagger-ui.css")


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI()
connect("postit")
secret = "secret-key"
manager = LoginManager(secret, "/auth/token")


@manager.user_loader
def load_user(user_name: str):
    user = User.objects(user_name=user_name).first()
    return user


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "success": True,
        "message": "hello, world",
        "data": {}
    }


@app.post("/auth/token")
def login(data: OAuth2PasswordRequestForm = Depends()):
    user_name = data.username
    password = data.password

    user = load_user(user_name)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=user_name)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users", response_model=UserOut)
def create_user(user_in: UserIn):
    user_in.password = bcrypt.hashpw(
        user_in.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_out = db_utils.create_user(user_in=user_in)
    return UserOut(
        pk=str(user_out.id),
        first_name=user_out.first_name,
        last_name=user_out.last_name,
        user_name=user_out.user_name,
        email=user_out.email
    )


@app.get("/users/all")
async def get_all_users() -> List[UserOut]:
    users = db_utils.get_users()
    user_list = []
    for user in users:
        user_out = UserOut(
            pk=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name,
            email=user.email
        )
        user_list.append(user_out)
    return {
        "success": True,
        "message": "users found",
        "data": user_list
    }


@app.get("/users/{user_name}")
async def get_user(user_name: str) -> UserOut:
    user = db_utils.get_user(user_name=user_name)
    if user:
        return {
            "success": True,
            "message": "user found",
            "data": UserOut(
                pk=str(user.id),
                first_name=user.first_name,
                last_name=user.last_name,
                user_name=user.user_name,
                email=user.email
            )
        }
    return {
        "success": False,
        "message": "user does not exist",
        "data": {}
    }
