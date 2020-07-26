from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Tuple, Dict
from datetime import datetime


class UserIn(BaseModel):
    first_name: str = Field(..., title="first name",
                            description="the first name of the user")
    last_name: Optional[str] = Field(
        None, title="last name", description="the last name of the user")
    user_name: str = Field(..., title="user name",
                           description="the user name of the user")
    email: EmailStr = Field(..., title="email",
                            description="the email of the user")
    password: str = Field(..., title="password",
                          description="the password of the user")


class UserOut(BaseModel):
    pk: str = Field(..., title="id",
                    description="the unique id (primary key) assigned to the user")
    first_name: str = Field(..., title="first name",
                            description="the first name of the user")
    last_name: Optional[str] = Field(
        None, title="last name", description="the last name of the user")
    user_name: str = Field(..., title="user name",
                           description="the user name of the user")
    email: EmailStr = Field(..., title="email",
                            description="the email of the user")


class PostIn(BaseModel):
    author: str = Field(..., title="post author",
                        description="the user who developed the post")
    title: str = Field(..., title="post title",
                       description="the title of the post")
    body: str = Field(..., title="post body",
                      description="the body of the post")


class PostOut(BaseModel):
    pk: str = Field(..., title="id",
                    description="the unique id (primary key) assigned to the post")
    author: str = Field(..., title="post author",
                        description="the user who developed the post")
    title: str = Field(..., title="post title",
                       description="the title of the post")
    body: str = Field(..., title="post body",
                      description="the content of the post")
    date_defined: datetime = Field(..., title="date defined",
                                   description="the date the post was defined")
    likes: Optional[int] = Field(None, title="likes",
                                 description="the number of likes on the post")
    liked_by: Optional[List] = Field(None,  title="liked by",
                                     description="a list of users who liked the post")


class CommentIn(BaseModel):
    author: str = Field(..., title="comment author",
                        description="the user who developed the comment")
    post: str = Field(..., tite="post id",
                      description="the id of the post on which the comment was classined")
    comment: str = Field(..., title="comment",
                         description="the comment on a post")


class CommentOut(BaseModel):
    pk: str = Field(..., title="id",
                    description="the unique id (primary key) assigned to the comment")
    author: str = Field(..., title="post author",
                        description="the user who classined the comment")
    post: str = Field(..., tite="post id",
                      description="the id of the post on which the comment was classined")
    comment: str = Field(..., title="comment",
                         description="the comment on a post")
    date_defined: datetime = Field(..., title="date defined",
                                   description="the date the comment was defined")
    likes: Optional[int] = Field(
        None, title="likes", description="the number of likes on the comment")
    liked_by: Optional[List] = Field(None,  tite="liked by",
                                     description="a list of users who liked the comment")
