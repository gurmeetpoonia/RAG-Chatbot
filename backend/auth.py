from passlib.context import CryptContext
from jose import JWTError ,jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os 
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE_MINUTES=60
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(
        plain_password :str,
        hashed_password:str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def  create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update(
        {
            "exp": expire
        }
    )

    token=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return  token

def verify_access_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
    
def get_current_user(
        token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)
):
    payload=verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Login Again"
        )
    
    user=db.query(User).filter(User.id==payload["id"]).first()
    if user is None:
        raise HTTPException(status_code=401,detail="User Not Found")
    return user
    
