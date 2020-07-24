from fastapi import FastAPI, Path, Query, Body
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field
from mongoengine import connect, Document, StringField


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
connect("testdb")


class User(Document):
    first_name: str = StringField(required=True)
    last_name: str = StringField(required=False)
    user_name: str = StringField(required=True, unique=True)
    password: str = StringField(required=True)


class UserIn(BaseModel):
    first_name: str = Field(..., title="first name")
    last_name: Optional[str] = Field(None, title="last name")
    user_name: str = Field(..., title="user name")
    password: str = Field(..., title="password")


class UserOut(BaseModel):
    pk: str = Field(..., title="id")
    first_name: str = Field(..., title="first name")
    last_name: Optional[str] = Field(None, title="last name")
    user_name: str = Field(..., title="user name")


@app.post("/user", response_model=UserOut)
async def post_user(user_in: UserIn) -> Dict[str, str]:
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name,
        password=user_in.password
    )
    user.save()
    user_out = UserOut(
        pk=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        user_name=user.user_name
    )
    return user_out


@app.get("/user", response_model=List[UserOut])
async def get_all_users() -> List[UserOut]:
    users = User.objects()
    user_list = []
    for user in users:
        user_out = UserOut(
            pk=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name
        )
        user_list.append(user_out)
    return user_list


@app.get("/user/{user_name}", response_model=UserOut)
async def get_user(user_name: str) -> UserOut:
    user = User.objects(user_name=user_name).first()
    print(user.pk)
    if user:
        return UserOut(
            pk=str(user.pk),
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name
        )
    return {"message": "user does not exist"}
