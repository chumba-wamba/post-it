from typing import Optional, List, Tuple, Dict
from body_models import UserIn, UserOut, PostIn, PostOut, CommentIn, CommentOut
from db_models import User, Post, Comment


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
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name,
        email=user_in.email,
        password=user_in.password
    )
    user.save()
    return user


def get_post(id):
    post = Post.objects(id=id)


def get_posts_by_user(user_name: str):
    posts = Post.objects(user_name=user_name)
    return posts


def get_posts():
    posts = Post.objects()
    return posts


def create_post(post_in: PostIn):
    post = Post(
        author=post_in.author,
        title=post_in.title,
        body=post_in.body
    )
    post.save()
    return post


def get_comment(id):
    comment = Comment.objects(id=id)


def get_comments_by_user(user_name: str):
    comments = Comment.objects(author=user_name)
    return comments


def get_comment_by_post(post):
    comments = Comment.objects(post=post)
    return comments


def get_comments():
    comments = Comment.objects()
    return comments


def create_comment(comment_in: CommentIn):
    comment = Comment(
        author=comment_in.author,
        post=comment_in.post,
        comment=comment_in.comment
    )
    comment.save()
    return comment
