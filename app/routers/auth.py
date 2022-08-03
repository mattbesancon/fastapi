from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schema, models, oauth2
from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = "4dee5112e82b454ea63ceecc9e50a333bd0a55f3eb97858098ef9a20841d5e0c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=404, detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

