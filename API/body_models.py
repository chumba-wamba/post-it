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
    _id = Field(..., title="id",
                description="the unique id (primary key) assigned to the user")
    first_name: str = Field(..., title="first name",
                            description="the first name of the user")
    last_name: Optional[str] = Field(
        None, title="last name", description="the last name of the user")
    user_name: str = Field(..., title="user name",
                           description="the user name of the user")
    email: str = Field(..., title="email", description="the email of the user")


def PostIn(BaseModel):
    author: str = Field(..., title="post author",
                        description="the user who developed the post")

    title: str = Field(..., title="post title",
                       description="the title of the post")
    body: str = Field(..., title="post title",
                      description="the title of the post")


def PostOut(BaseModel):
    _id = Field(..., title="id",
                description="the unique id (primary key) assigned to the post")
    author: str = Field(..., title="post author",
                        description="the user who developed the post")
    title: str = Field(..., title="post title",
                       description="the title of the post")
    body: str = Field(..., title="post body",
                      description="the content of the post")
    date_defined = Field(..., "date defined",
                         description="the date the post was defined")
    likes: Optional[int] = Field(None, "likes",
                                 description="the number of likes on the post")
    liked_by: Optional[List] = Field(None,  tite="liked by",
                                     description="a list of users who liked the post")


def CommentIn(BaseModel):
    author: str = Field(..., title="comment author",
                        description="the user who developed the comment")
    post = Field(..., tite="post id",
                           description="the id of the post on which the comment was defined")
    comment: str = Field(..., title="comment",
                         description="the comment on a post")


def CommentOut(BaseModel):
    _id = Field(..., title="id",
                description="the unique id (primary key) assigned to the comment")
    author: str = Field(..., title="post author",
                        description="the user who defined the comment")
    post = Field(..., tite="post id",
                           description="the id of the post on which the comment was defined")
    comment: str = Field(..., title="comment",
                         description="the comment on a post")
    date_defined: str = Field(..., title="date defined",
                              description="the date the comment was defined")
    likes: Optional[int] = Field(
        None, title="likes", description="the number of likes on the comment")
    liked_by: Optional[List] = Field(None,  tite="liked by",
                                     description="a list of users who liked the comment")
