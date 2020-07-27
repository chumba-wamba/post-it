from typing import Optional, List, Tuple, Dict
from pydantic import EmailStr
from body_models import UserIn, UserOut, PostIn, PostOut, CommentIn, CommentOut
from db_models import User, Post, Comment


def create_user(user_in: UserIn) -> User:
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
        return None


def get_users() -> List[User]:
    users = User.objects()
    return users


def get_user(user_name: str):
    user = User.objects(user_name=user_name).first()
    return user


def get_user_by_email(email: EmailStr) -> User:
    user = User.objects(email=email).first()
    return user


def delete_user(user_name: str) -> bool:
    user = User.objects(user_name=user_name).first()
    if user:
        user.delete()
        return True
    return False


def create_post(post_in: PostIn) -> Post:
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
            return None


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
        return None


def delete_post(post_id: str) -> bool:
    post = Post.objects(pk=post_id).first()
    if post:
        post.delete()
        return True
    return False


def create_comment(comment_in: CommentIn):
    author, post = get_user(user_name=comment_in.author), get_post(
        post_id=comment_in.post)
    if author and post:
        comment = Comment(
            author=comment_in.author,
            post=comment_in.post,
            comment=comment_in.comment
        )
        try:
            comment.save()
            return comment
        except:
            return None


def get_comments_by_post(post_id: str):
    try:
        comments = Comment.objects(post=post_id)
        return comments
    except:
        return None


def get_comments_by_author(author: str):
    comments = Comment.objects(author=author)
    return comments


def get_comment(comment_id):
    try:
        comment = Comment.objects(pk=comment_id)
        return comment
    except:
        return None
