from fastapi import FastAPI, Path, Query, Body
from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field

# Initialising an object for the FastAPI class
# as app; app will be responsible for taking care
# of all the routes and is the most essential
# entity of the entire code
# app also happens to be the entry point for the
# uvicorn server to access the entire API codebase
# At the same time, app is used to create routes
# which along with the parsing functionality provided
# by the pydantic module helps creating swagger-ui
# and redoc based auto-documentation
# The auto-documentation feature along with the async
# nature of the framework is probably the reason
# why one would want to move from flask to fast-api
# to create their APIs; sanic also happens to be an
# alternative which allows using async code but
# fastapi reigns dominant for now
app = FastAPI()


# This is a get request for the URI end-point "/"
# and returns a dictionary (parsed to JSON) with
# the key of "message" and the value of "hello, world!"
# You can also add a dynamic functionality to the
# URI end-point via using something known as the path
# parameters and spice up the way the user interacts
# with the end-point with query parameters
@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "hello, world!"}


# Path pararmeters and query parameters are implemented
# in fastapi with the help of the Path and Query
# objects in the endpoint definition; they work with
# both Get and Post requests (and the other types that
# exist)
@app.get("/book/{author_name}")
def get_book(
    author_name: str = Path(..., title="author name"),
    published_books: bool = Query(
        None, title="published books", description="number of books published by the author"),
) -> Dict:
    if published_books:
        return {
            "author_name": author_name,
            "published_books": {
                "one": "test_one",
                "two": "test_two",
                "three": "test_three"
            }
        }
    return {"author_name": author_name}


# In case of using path queries, the biggest issue
# that may arise is having to use a static path with
# the same beggining as the dynamic one
# In this case, it is essential to have the static path
# before the dynamic path, as the framework renders
# the paths from the top to the bottom and otherwise
# the static path may be confused to arise from the
# dynamic one with the latter portion of the path
# as the user information
@app.get("/test/static")
def get_static() -> Dict[str, str]:
    return {"message": "static"}


@app.get("/test/{dynamic}")
def get_dynamic(dynamic: str = Path(..., title="dynamic")) -> Dict[str, str]:
    return {
        "message": "dynamic",
        "path_parameter": dynamic
    }


# There might be times when you might want to send
# data discretely and not want it to be a part of the
# URL
# In this case sending data as post requests is ideal;
# wherein the request body itself encapsulates all the
# data and a HTTPS server will have the request body
# hashed and hence secure from any external snooping
# fastapi makes use of the Body object in this case

# To be able to work with post requests, you need to
# create a class with all the parameters of the request
# and have this class inherit from pydantic's BadeModel
# for auto-documentation and editor support
class Test(BaseModel):
    first: int = Field(...)
    second: Optional[int] = Field(None)
    third: Optional[int] = Field(None)


@app.post("/test/post")
def post_body(test: Test) -> Test:
    return test


# To actually start the server, enter the directory
# where the main.py file is present and enter the
# following command on the terminal:
# uvicorn main:app --reload
