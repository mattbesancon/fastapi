from hashlib import new
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title 1", "content": "content 1", "id": 1}, {"title": "title 2", "content": "content 2", "id": 2}]    

@app.get("/")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = (dict(post))
    post_dict["id"] = randrange(10000000)
    my_posts.append(post_dict)
    return {
        "data": post_dict
    }

@app.get("/posts/{id}")
def get_post(id):
    post_id = list(filter(None, [x if x["id"] == int(id) else None for x in my_posts]))
    return {
        "data": post_id
    }

