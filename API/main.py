from fastapi import FastAPI, Path, Query, Body, Depends
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field
from API.body_models import UserIn, UserOut, PostIn, PostOut, CommentIn, CommentOut
from API.db_models import User, Post, Comment


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


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "success": True,
        "message": "hello, world",
        "data": {}
    }
