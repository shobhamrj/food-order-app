import jwt
from passlib.hash import bcrypt
from datetime import timedelta, datetime
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import User
from fastapi import Depends, HTTPException
from db import cursor, mysql_conn
from config import settings

# JWT Configuration
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 4300  # 12 hour

security = HTTPBearer()


def authenticate_user(email: str, password: str) -> User:
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.verify(password, user[3]):
        return user


def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="Invalid token")
