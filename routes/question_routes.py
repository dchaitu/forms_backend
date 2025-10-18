from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from enums import QuestionType
from models import Question, engine, Option
from schema import QuestionCreate, QuestionDTO, QuestionUpdate

router = APIRouter(prefix='/question', tags=['Question'])


@router.post("/create/", response_model=QuestionDTO)
def create_question(question_create: QuestionCreate):
    """
    Create a new question.
    Assumes QuestionCreate schema contains `section_id` and `options: list[str]`.
    """
    with Session(engine) as session:
        question_data = question_create.model_dump()
        option_texts = question_data.pop('options', None)

        db_question = Question(**question_data)

        if question_create.question_type in [QuestionType.MULTIPLE_CHOICE, QuestionType.CHECKBOXES, QuestionType.DROPDOWN]:
            if option_texts:
                for option_text in option_texts:
                    db_question.options.append(Option(text=option_text))
        
        session.add(db_question)
        session.commit()
        session.refresh(db_question)
        return db_question

@router.get("/{question_id}", response_model=QuestionDTO)
def get_question(question_id: int):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question

@router.put("/{question_id}", response_model=QuestionDTO)
def update_question(question_id: int, question_update: QuestionUpdate):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        update_data = question_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(question, key, value)

        session.add(question)
        session.commit()
        session.refresh(question)
        return question

@router.delete("/{question_id}")
def delete_question(question_id: int):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        session.delete(question)
        session.commit()
    return {"message": "Question deleted successfully"}