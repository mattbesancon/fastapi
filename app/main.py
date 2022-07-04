from hashlib import new
from fastapi import Depends, FastAPI, HTTPException, Response
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
def create_posts(post: Post, db: Session = Depends(get_db)):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {
        "data": db_post
    }



@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {
        "data": post
    }



@app.delete("/posts/{id}", status_code=204, response_class=Response)
def delete_post(id: int, db: Session = Depends(get_db)):
    del_post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(del_post)
    db.commit()
    return None


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cur.execute("UPDATE posts SET title = %s, content = %s WHERE ID = %s RETURNING *", (post.title, post.content, id))
    updated_post = cur.fetchone()
    if not updated_post:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    return {
        "data": updated_post
    }

