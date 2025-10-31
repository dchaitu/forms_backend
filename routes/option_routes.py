from fastapi import APIRouter, HTTPException, UploadFile, File
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

@router.put("/{question_id}", response_model=list[OptionDTO])
def update_options(question_id: int, options_update: list[OptionUpdate]):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        existing_options = {opt.id: opt for opt in question.options}
        incoming_ids = {opt.id for opt in options_update if opt.id}

        # update and add
        for opt_data in options_update:
            if opt_data.id in existing_options:
                existing_options[opt_data.id].text = opt_data.text
            else:
                session.add(Option(text=opt_data.text, question_id=question_id))

        # delete removed
        for opt_id in set(existing_options.keys()) - incoming_ids:
            session.delete(existing_options[opt_id])

        session.commit()
        updated = session.query(Option).filter(Option.question_id == question_id).all()
        return [OptionDTO.model_validate(o) for o in updated]

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


@router.post("/upload_image/{option_id}")
def upload_option_image(option_id: int, file: UploadFile = File(...)):
    with Session(engine) as session:
        option = session.get(Option, option_id)
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        option.option_image = file.file.read()
        session.commit()
    return {"message": "Option image uploaded successfully"}
