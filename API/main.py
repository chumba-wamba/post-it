from fastapi import FastAPI, Path, Query, Body, Depends
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from mongoengine import connect
import bcrypt
from typing import Optional, List, Tuple, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from body_models import UserIn, UserOut, PostIn, PostOut, CommentIn, CommentOut
from db_models import User, Post, Comment
import db_utils


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the async default values for the swagger js and css.
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
async def root(user=Depends(manager)) -> Dict[str, str]:
    return {
        "success": True,
        "message": "hello, world",
        "data": {}
    }


@app.post("/auth/token")
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    user_name = data.username
    password = data.password

    user = load_user(user_name)
    if not user:
        raise InvalidCredentialsException
    elif not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=user_name)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users")
async def create_user(user_in: UserIn) -> Dict[str, Any]:
    user_in.password = bcrypt.hashpw(
        user_in.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_out = db_utils.create_user(user_in=user_in)
    if user_out:
        return {
            "success": True,
            "message": "user created successfully",
            "data":  UserOut(
                pk=str(user_out.id),
                first_name=user_out.first_name,
                last_name=user_out.last_name,
                user_name=user_out.user_name,
                email=user_out.email
            )}
    return {
        "success": False,
        "message": "could not create user",
        "data": {}
    }


@app.get("/users/all")
async def get_all_users() -> Dict[str, Any]:
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


@app.get("/users/user_name/{user_name}")
async def get_user(user_name: str) -> Dict[str, Any]:
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


@app.get("/users/email/{email}")
async def get_user_by_email(email: EmailStr) -> Dict[str, Any]:
    user = db_utils.get_user_by_email(email=email)
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


@app.get("/users/delete/{user_name}")
async def delete_user(user_name: str) -> Dict[str, Any]:
    deleted = db_utils.delete_user(user_name)
    if deleted:
        return {
            "success": True,
            "message": "user deleted successfully",
            "data": {}
        }
    return {
        "success": False,
        "message": "user does not exist",
        "data": {}
    }


@app.put("/users/update/{user_name}")
async def update_user():
    pass


@app.post("/posts")
async def create_post(post_in: PostIn) -> Dict[str, Any]:
    post = db_utils.create_post(post_in=post_in)
    if post:
        return {
            "success": True,
            "message": "post successfully created",
            "data":  PostOut(
                pk=str(post.pk),
                author=post.author,
                title=post.title,
                body=post.body,
                date_defined=post.date_defined,
                likes=post.likes,
                liked_by=post.liked_by
            )}
    return {
        "success": False,
        "message": "could not create user",
        "data": {}
    }


@app.get("/posts/all/{author}")
async def get_posts_by_author(author: str):
    posts = db_utils.get_posts_by_author(author=author)
    if not posts:
        return {
            "success": False,
            "message": "author does not exist",
            "data": {}
        }
    post_list = []
    for post in posts:
        post_out = PostOut(
            pk=str(post.pk),
            author=post.author,
            title=post.title,
            body=post.body,
            date_defined=post.date_defined,
            likes=post.likes,
            liked_by=post.liked_by
        )
        post_list.append(post_out)
    return {
        "success": True,
        "message": "posts found",
        "data": post_list
    }


@app.get("/posts/{post_id}")
async def get_post(post_id):
    post = db_utils.get_post(post_id)
    if post:
        return {
            "success": True,
            "message": "post found",
            "data": PostOut(
                pk=str(post.pk),
                author=post.author,
                title=post.title,
                body=post.body,
                date_defined=post.date_defined,
                likes=post.likes,
                liked_by=post.liked_by
            )}
    return {
        "success": False,
        "message": "post does not exist",
        "data": {}
    }


@app.get("/posts/delete/{post_id}")
async def delete_post(post_id):
    deleted = db_utils.delete_post(post_id)
    if deleted:
        return {
            "success": True,
            "message": "post successfully deleted",
            "data": {}
        }
    return {
        "success": False,
        "message": "post does not exist",
        "data": {}
    }


@app.put("/posts/update/{post_id}")
async def update_post():
    pass


@app.post("/comments")
async def create_comment(comment_in: CommentIn) -> Dict[str, Any]:
    comment = db_utils.create_comment(comment_in=comment_in)
    if comment:
        return {
            "success": True,
            "message": "comment successfully created",
            "data":  CommentOut(
                pk=str(comment.pk),
                author=comment.author,
                post_id=str(comment.post_id),
                comment=comment.comment,
                date_defined=comment.date_defined,
                likes=comment.likes,
                liked_by=comment.liked_by
            )}
    return {
        "success": False,
        "message": "could not create comment",
        "data": {}
    }


@app.get("/comments/all/{post_id}")
async def get_comments_by_post(post_id: str):
    comments = db_utils.get_comments_by_post(post_id=post_id)
    if not comments:
        return {
            "success": False,
            "message": "could not find comments",
            "data": {}
        }
    comment_list = []
    for comment in comments:
        post_out = CommentOut(
            pk=str(comment.pk),
            author=comment.author,
            post_id=str(comment.post_id),
            comment=comment.comment,
            date_defined=comment.date_defined,
            likes=comment.likes,
            liked_by=comment.liked_by
        )
        comment_list.append(post_out)
    return {
        "success": True,
        "message": "comments found",
        "data": comment_list
    }


@app.get("/comments/delete/{comment_id}")
async def delete_comment(comment_id: str):
    deleted = db_utils.delete_comment(comment_id=comment_id)
    if deleted:
        return {
            "success": True,
            "message": "comment successfully deleted",
            "data": {}
        }
    return {
        "success": False,
        "message": "could not delete comment",
        "data": {}
    }


@app.get("/comments/delete/all/{post_id}")
async def delete_comments_by_post(post_id: str):
    deleted = db_utils.delete_comments_by_post(post_id=post_id)
    if deleted:
        return {
            "success": True,
            "message": "comments successfully deleted",
            "data": {}
        }
    return {
        "success": False,
        "message": "could not delete comments",
        "data": {}
    }


@app.get("/comments/delete/all/{author}")
async def delete_comments_by_author(author: str):
    deleted = db_utils.delete_comments_by_author(author)
    if deleted:
        return {
            "success": True,
            "message": "comments successfully deleted",
            "data": {}
        }
    return {
        "success": False,
        "message": "could not delete comments",
        "data": {}
    }
