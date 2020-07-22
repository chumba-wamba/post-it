from fastapi import FastAPI, Path, Query, Body
from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field
from mongoengine import connect, Document, StringField

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
    first_name: str = Field(..., title="first name")
    last_name: Optional[str] = Field(None, title="last name")
    user_name: str = Field(..., title="user name")


@app.post("/user")
async def post_user(user_in: UserIn) -> Dict[str, str]:
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name,
        password=user_in.password
    )
    user.save()
    user_out = UserOut(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name
    )
    return user_out


@app.get("/user")
async def get_all_users() -> List[UserOut]:
    users = User.objects()
    user_list = []
    for user in users:
        user_out = UserOut(
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name
        )
        user_list.append(user_out)
    return user_list


@app.get("/user/{user_name}")
async def get_user(user_name: str) -> UserOut:
    user = User.objects(user_name=user_name).first()
    return UserOut(
        first_name=user.first_name,
        last_name=user.last_name,
        user_name=user.user_name
    )
