from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

app = FastAPI()
SECRET = "secret-key"
manager = LoginManager(SECRET, "/auth/token")
fake_db = {
    "nisarg42": {
        "password": "password"
    }
}


@manager.user_loader
def load_user(password: str):
    user = fake_db.get(password)
    return user


@app.post("/auth/token")
def login(data: OAuth2PasswordRequestForm = Depends()):
    user_name = data.username
    password = data.password

    user = load_user(user_name)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=user_name)
    )
    return {"access_token": access_token, "token_type": "bearer"}
