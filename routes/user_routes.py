from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models import User, engine, Form
from schema import UserCreate, UserDTO, FormDTO

router = APIRouter(prefix='/user', tags=['User'])




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


@router.get("/{user_id}/forms")
def get_user_forms(user_id: int)-> list[FormDTO]:
    with Session(engine) as session:
        forms = (
            session.query(Form)
            .join(Form.user)
            .filter(User.user_id == user_id)
            .options(joinedload(Form.user))
            .all()
        )
        forms_dtos = [FormDTO.model_validate(form) for form in forms]
        return forms_dtos