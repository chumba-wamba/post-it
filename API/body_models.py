from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field


def UserIn(BaseModel):
    first_name: str = Field(..., title="first name",
                            description="the first name of the user")
    last_name: Optional[str] = Field(
        None, title="last name", description="the last name of the user")
    user_name: str = Field(..., title="user name",
                           description="the user name of the user")
    email: str = Field(..., title="email", description="the email of the user")
    password: str = Field(..., title="password",
                          description="the password of the user")


def UserOut(BaseModel):
    first_name: str = Field(..., title="first name",
                            description="the first name of the user")
    last_name: Optional[str] = Field(
        None, title="last name", description="the last name of the user")
    user_name: str = Field(..., title="user name",
                           description="the user name of the user")
    email: str = Field(..., title="email", description="the email of the user")
    posts: List = Field(..., title="posts",
                        decription="the posts written by the user")


def PostInt(BaseModel):
    title: str = Field(..., title="post title",
                       description="the title of the post")
    post: str = Field(..., title="post title",
                      description="the title of the post")


def PostOut(BaseModel):
    title: str = Field(..., title="post title",
                       description="the title of the post")
    body: str = Field(..., title="post body",
                      description="the content of the post")
    date_defined = Field(..., "date defined",
                         description="the date the post was defined")
    likes: int = Field(..., "likes",
                       description="the number of likes on the post")
    comments: List = Field(..., title="comments",
                           description="the comments on the post")
