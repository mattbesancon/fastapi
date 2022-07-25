from fastapi import Depends, HTTPException, APIRouter
from .. import models, schema
from ..database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


router = APIRouter()


SECRET_KEY = "4dee5112e82b454ea63ceecc9e50a333bd0a55f3eb97858098ef9a20841d5e0c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# value is not a valid dict
@router.post("/users", status_code=201)
def create_users(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "data": db_user
    }


@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"the user with id {id} does not exist")

    return {
        "data": user
    }

