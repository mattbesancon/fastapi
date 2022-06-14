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

@app.post("/createposts")
def create_posts(new_post: Post):
    print(dict(new_post))
    return {
        "data": new_post
    }

