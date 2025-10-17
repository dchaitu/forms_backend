from fastapi import APIRouter
from sqlalchemy.orm import Session

from models import Question, engine
from schema import QuestionCreate

router = APIRouter(prefix='/question', tags=['Question'])


# def create_options(option_ids: list[int]):
#     with Session(engine) as session:
#         options = session.scalars(select(Option).where(Option.id.in_(option_ids))).all()
#         return options

@router.post("/create/")
def create_question(question: QuestionCreate):
    option_objs = []


    question_obj = Question(
        question_type=question.question_type,
        form_id=question.form_id,
        text=question.text,
        option_ids=question.option_ids
    )

