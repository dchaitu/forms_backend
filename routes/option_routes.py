from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from enums import QuestionType
from models import Option, engine, Question
from schema import OptionCreate, OptionDTO, OptionUpdate

router = APIRouter(prefix='/option', tags=['Option'])

@router.post("/create/", response_model=OptionDTO)
def create_option(option: OptionCreate):
    with Session(engine) as session:
        question = session.get(Question, option.question_id)
        if question.question_type in [QuestionType.MULTIPLE_CHOICE, QuestionType.CHECKBOXES, QuestionType.DROPDOWN]:
            option = Option(
                text=option.text,
                question_id=option.question_id,
            )
            session.add(option)
            session.commit()
            option_dto = OptionDTO.model_validate(option)
        else:
            raise HTTPException(status_code=400, detail="Question type does not support options")

    return option_dto

@router.put("/", response_model=OptionDTO)
def update_option(option_update:OptionUpdate):
    with Session(engine) as session:
        option = session.get(Option, option_update.option_id)
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")

        option.text = option_update.text
        session.add(option)
        session.commit()
        session.refresh(option)
        return OptionDTO.model_validate(option)

@router.delete("/{option_id}")
def delete_option(option_id: int):
    with Session(engine) as session:
        option = session.get(Option, option_id)
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        session.delete(option)
        session.commit()
    return {"message": "Option deleted successfully"}


@router.get("/all/", response_model=list[OptionDTO])
def get_all_options():
    with Session(engine) as session:
        options = session.query(Option).all()
        return [OptionDTO.model_validate(option) for option in options]