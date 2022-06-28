from hashlib import new
from fastapi import FastAPI, HTTPException
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
    posts = cur.fetchall()
    print(posts)
except Exception as error:
    print("cannot connect to db, error:", error)


@app.get("/")
def get_posts():
    return {"data": posts}


@app.post("/posts", status_code=201)
def create_posts(post: Post):
    cur.execute("INSERT INTO POSTS (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content))
    new_post = cur.fetchone()
    conn.commit()
    return {
        "data": new_post
    }


@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("SELECT * FROM POSTS where ID = %s", (id,))
    post = cur.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    return {
        "data": post
    }


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    cur.execute("DELETE FROM POSTS where ID = %s RETURNING *", (id,))
    del_post = cur.fetchone()
    conn.commit()
    if not del_post:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")



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

