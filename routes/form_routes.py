from fastapi import APIRouter
from sqlalchemy.orm import Session

from models import Form, engine
from schema import FormCreate, FormDTO

router = APIRouter(prefix='/form', tags=['Form'])


@router.post("/create/")
def create_form(form_dto: FormCreate):
    with Session(engine) as session:
        form = Form(
            title=form_dto.title,
            description=form_dto.description,
            created_by=form_dto.created_by,
            questions=form_dto.questions
        )
        session.add(form)
        session.commit()
        form_dto = FormDTO.model_validate(form)
    return form_dto

