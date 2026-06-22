from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY="CHANGE_ME"
ALGORITHM="HS256"

def hash_password(password:str):
    return pwd.hash(password)

def verify_password(password, hashed):
    return pwd.verify(password, hashed)

def create_access_token(data:dict, minutes:int=60):
    payload=data.copy()
    payload["exp"]=datetime.utcnow()+timedelta(minutes=minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
