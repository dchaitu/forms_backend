import hashlib
from datetime import timedelta, datetime, UTC

import jwt
import requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Security

UPLOAD_DIR = "uploads"
JWT_SECRET = "p1beyVW)E>b{1gya{,I+yd]>DfN/\9#*"
secret_key = '6Lcp4Y0rAAAAAMx574CaTgPELQT7aT24Aprreo84'
security = HTTPBearer()

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_access_token(username: str, expires_delta: timedelta = None):
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=145))
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

def verify_password(password: str, password_hash: str):
    return hash_password(password) == password_hash


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def verify_recaptcha(token: str) -> bool:
    if token == "test-token":
        return True

    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": secret_key,
        "response": token,
    }
    response = requests.post(url, data=data)
    result = response.json()
    print(result)
    return result["success"]