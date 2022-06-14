from hashlib import new
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"hello": "welcome to my api"}

@app.post("/posts")
def create_posts(post: Post):
    print(dict(post))
    return {
        "data": post
    }

