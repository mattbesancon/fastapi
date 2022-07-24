from fastapi import Depends, HTTPException, Response, APIRouter
from pydantic import BaseModel
from .. import models, schema
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


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

   

@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {
        "data": posts
    }


@router.post("/posts", status_code=201, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {
        "data": db_post
    }


@router.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    return {
        "data": post
    }


@router.delete("/posts/{id}", status_code=204, response_class=Response)
def delete_post(id: int, db: Session = Depends(get_db)):
    del_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not del_post:
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    db.delete(del_post)
    db.commit()
    return None


@router.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=404, detail=f"the post with id {id} does not exist")

    post_query.update(dict(post))
    db.commit()
    return {
        "data": post_query.first()
    }

