from typing import Optional, List, Tuple, Dict
from pydantic import EmailStr
from body_models import UserIn, UserOut, PostIn, PostOut, CommentIn, CommentOut
from db_models import User, Post, Comment


def create_user(user_in: UserIn):
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        user_name=user_in.user_name,
        email=user_in.email,
        password=user_in.password
    )
    try:
        user.save()
        return user
    except:
        return False


def get_users():
    users = User.objects()
    return users


def get_user(user_name: str):
    user = User.objects(user_name=user_name).first()
    return user


def get_user_by_email(email: EmailStr):
    user = User.objects(email=email).first()
    return user


def delete_user(user_name: str) -> bool:
    user = User.objects(user_name=user_name).first()
    if user:
        user.delete()
        return True
    return False


def create_post(post_in: PostIn):
    author = get_user(user_name=post_in.author)
    if author:
        post = Post(
            author=post_in.author,
            title=post_in.title,
            body=post_in.body
        )
        try:
            post.save()
            return post
        except:
            return False


def get_posts_by_author(author: str):
    if User.objects(user_name=author).first():
        posts = Post.objects(author=author)
        return posts
    return False


def get_post(post_id):
    try:
        post = Post.objects(pk=post_id).first()
        return post
    except:
        return False


def delete_post(post_id: str):
    post = Post.objects(pk=post_id).first()
    if post:
        post.delete()
        return True
    return False


def create_comment(comment_in: CommentIn):
    author, post = get_user(user_name=comment_in.author), get_post(
        post_id=comment_in.post_id)
    if author and post:
        comment = Comment(
            author=comment_in.author,
            post_id=comment_in.post_id,
            comment=comment_in.comment
        )
        try:
            comment.save()
            return comment
        except:
            return False


def get_comments_by_post(post_id: str):
    try:
        comments = Comment.objects(post_id=post_id)
        return comments
    except:
        return False


def get_comments_by_author(author: str):
    comments = Comment.objects(author=author)
    return comments


def get_comment(comment_id: str):
    try:
        comment = Comment.objects(pk=comment_id)
        return comment
    except:
        return False


def delete_comment(comment_id: str):
    comment = Comment.objects(pk=comment_id)
    if comment:
        comment.delete()
        return True
    return False


def delete_comments_by_post(post_id: str):
    post = Post.objects(pk=post_id)
    if post:
        comments = Comment.objects(post_id=post_id)
        for comment in comments:
            comment.delete()
            return True
    return False


def delete_comments_by_author(author: str):
    user = User.objects(user_name=author)
    if user:
        comments = Comment.objects(author=author)
        for comment in comments:
            comment.delete()
            return True
    return False
