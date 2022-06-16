from hashlib import new
from fastapi import FastAPI, HTTPException
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

@app.post("/posts", status_code=201)
def create_posts(post: Post):
    post_dict = (dict(post))
    post_dict["id"] = randrange(10000000)
    my_posts.append(post_dict)
    return {
        "data": post_dict
    }

@app.get("/posts/{id}")
def get_post(id: int):
    post_id = [x for x in my_posts if x["id"] == int(id)]
    
    if not post_id:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    return {
        "data": post_id
    }

