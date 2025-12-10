import os
from datetime import timedelta

from fastapi import FastAPI, HTTPException
from mangum import Mangum
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from constants import UPLOAD_DIR, hash_password, verify_password, create_access_token
from models import User, engine
from routes.user_routes import router as user_router
from routes.form_routes import router as form_router
from routes.section_routes import router as section_router
from routes.question_routes import router as question_router
from routes.option_routes import router as option_router
from routes.response_routes import router as response_router
from schema import UserDTO, UserCreate, UserLoginDTO, LoginDTO

app = FastAPI()
app.include_router(user_router)
app.include_router(form_router)
app.include_router(section_router)
app.include_router(question_router)
app.include_router(option_router)
app.include_router(response_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    '*'
]
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"),name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=UserDTO)
def create_user(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.query(User).filter(
            (User.username == user.username) | (User.email_address == user.email_address)
        ).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")
        hashed_password = hash_password(user.password)

        user_obj = User(
                    username=user.username,
                    fullname=user.fullname,
                    email_address=user.email_address,
                    password_hash=hashed_password,
                    pic_url=user.pic_url
                    )
        session.add(user_obj)
        session.commit()
        session.refresh(user_obj)
        user_dto = UserDTO.model_validate(user_obj)


    return user_dto

@app.get("/users")
def get_all_users():
    with Session(engine) as session:
        users = session.query(User).all()
        return [UserDTO.model_validate(user) for user in users]

@app.post("/login")
def login_user(user_info: UserLoginDTO):
    with Session(engine) as session:
        user_obj = session.query(User).filter(User.username == user_info.username).first()
        if not user_obj:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        print(f"user details {user_obj.__dict__}")
        print("user password ", user_obj.password_hash)
        print("user_info password ", user_info.password)
        if user_obj.password_hash != hash_password(user_info.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(user_info.username)
        refresh_token = create_access_token(user_info.username, timedelta(days=30))

        return LoginDTO(
            user_id=user_obj.user_id,
            username=user_obj.username,
            fullname=user_obj.fullname,
            email_address=user_obj.email_address,
            pic_url=user_obj.pic_url,
            access_token=access_token,
            refresh_token=refresh_token
        )

def handler(event, context):
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

