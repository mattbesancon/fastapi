from hashlib import new
from fastapi import Depends, FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {
        "data": posts
    }



@app.post("/posts", status_code=201)
def create_posts(post: Post):
    cur.execute("INSERT INTO POSTS (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content))
    new_post = cur.fetchone()
    conn.commit()
    return {
        "data": new_post
    }


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
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
    cur.execute("UPDATE posts SET title = %s, content = %s WHERE ID = %s RETURNING *", (post.title, post.content, id))
    updated_post = cur.fetchone()
    if not updated_post:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    return {
        "data": updated_post
    }

