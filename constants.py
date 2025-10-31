import hashlib
from datetime import timedelta, datetime, UTC

import jwt

UPLOAD_DIR = "uploads"
JWT_SECRET = "p1beyVW)E>b{1gya{,I+yd]>DfN/\9#*"

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_access_token(username: str, expires_delta: timedelta = None):
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=145))
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

def verify_password(password: str, password_hash: str):
    return hash_password(password) == password_hash