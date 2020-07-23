from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField(label="First name", validators=[
                             DataRequired(), Length(max=20)])
    last_name = StringField(label="Last name")
    user_name = StringField(label="User name", validators=[
                            DataRequired(), Length(min=6, max=20)])
    email = StringField(label="Email", validators=[
        DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[
        DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField(label="Password", validators=[
        DataRequired(), Length(min=6, max=20), EqualTo("password")])
    register = SubmitField(label="Register")


class LoginForm(FlaskForm):
    user_name = StringField(label="User name", validators=[
                            DataRequired(), Length(min=6, max=20)])
    password = PasswordField(label="Password", validators=[
        DataRequired(), Length(min=6, max=20)])
    login = SubmitField(label="Login")


class PostForm(FlaskForm):
    title = StringField(label="title", validators=[
                        DataRequired(), Length(min=6, max=20)])
    body = TextAreaField(label="body", validators=[
                         DataRequired(), Length(max=500)])
    submit = SubmitField(label="Submit")


class CommentForm(FlaskForm):
    comment = TextAreaField(label="body", validators=[
        DataRequired(), Length(max=500)])
    submit = SubmitField(label="Submit")
