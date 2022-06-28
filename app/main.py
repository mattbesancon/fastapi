from hashlib import new
from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    records = cur.fetchall()
    print(records)
except Exception as error:
    print("cannot connect to db, error:", error)


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
    post_id = [x for x in my_posts if x["id"] == id]
    
    if not post_id:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    return {
        "data": post_id
    }


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    post_index = [i for i, el in enumerate(my_posts) if el["id"] == id]

    if not post_index:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")
    else:
        my_posts.pop(post_index[0])
        return Response(status_code=204)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = [i for i, el in enumerate(my_posts) if el["id"] == id]
    
    if not post_index:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    post_dict = (dict(post))
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return {
        "data": post_dict
    }

