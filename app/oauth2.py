from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "4dee5112e82b454ea63ceecc9e50a333bd0a55f3eb97858098ef9a20841d5e0c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])

        id = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schema.TokenData(id=id)

    except JWTError:
            raise credentials_exception

    return token_data

