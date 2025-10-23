from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from constants import hash_password
from models import User, engine
from schema import UserCreate, UserDTO

router = APIRouter(prefix='/user', tags=['User'])


@router.post("/create/", response_model=UserDTO)
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
                    password_hash=hashed_password
                    )
        session.add(user_obj)
        session.commit()
        session.refresh(user_obj)
        user_dto = UserDTO.model_validate(user_obj)


    return user_dto

@router.get("/all/")
def get_all_users() -> list[UserDTO]:
    with Session(engine) as session:
        query = select(User)
        users = session.scalars(query).all()
        users_dtos = [UserDTO.model_validate(user) for user in users]
        return users_dtos


@router.get("/{user_id}/")
def get_user(user_id: int)-> UserDTO:
    with Session(engine) as session:

        query = session.get(User, user_id)
        user_dto = UserDTO.model_validate(query)
        return user_dto


def get_user_by_username(username: str)-> UserDTO:
    with Session(engine) as session:
        query = select(User).where(User.username == username)
        user = session.scalar(query)
        user_dto = UserDTO.model_validate(user)
        return user_dto