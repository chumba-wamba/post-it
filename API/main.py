from fastapi import FastAPI, Path, Query, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "hello, world"}
