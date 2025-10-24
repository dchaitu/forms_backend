from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from enums import QuestionType
from models import Question, engine, Option
from schema import QuestionCreate, QuestionDTO, QuestionUpdate, OptionDTO

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
        question_type_enum = question_data.pop('question_type')

        db_question = Question(**question_data)
        db_question.question_type = QuestionType(question_type_enum)

        if question_create.question_type in [QuestionType.MULTIPLE_CHOICE, QuestionType.CHECKBOXES, QuestionType.DROPDOWN]:
            if option_texts:
                for option_text in option_texts:
                    db_question.options.append(Option(text=option_text))
        
        session.add(db_question)
        session.commit()
        session.refresh(db_question)
        
        question_dto = QuestionDTO(
            question_id=db_question.id,
            section_id=db_question.section_id,
            question_type=db_question.question_type,
            title=db_question.title,
            description=db_question.description,
            is_required=db_question.is_required,
            options=[option.text for option in db_question.options] if db_question.options else []
        )
        return question_dto

@router.get("/{question_id}", response_model=QuestionDTO)
def get_question(question_id: int):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return QuestionDTO(
            id=question.id,
            section_id=question.section_id,
            question_type=question.question_type,
            title=question.title,
            description=question.description,
            is_required=question.is_required,
            options=[option.text for option in question.options] if question.options else []
        )

@router.put("/{question_id}", response_model=QuestionDTO)
def update_question(question_id: int, question_update: QuestionUpdate):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        update_data = question_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(question, key, value)

        # Handle options if provided
        if question_update.options is not None:
            existing_options = {opt.id: opt for opt in question.options}
            incoming_ids = {opt.id for opt in question_update.options if opt.id}

            # Add or update options
            for opt_data in question_update.options:
                if opt_data.id in existing_options:
                    # Update existing option
                    existing_options[opt_data.id].text = opt_data.text
                else:
                    # Add new option
                    new_option = Option(text=opt_data.text, question_id=question.id)
                    session.add(new_option)

            # Delete options not in incoming list
            for opt_id in set(existing_options.keys()) - incoming_ids:
                session.delete(existing_options[opt_id])

        # Save changes
        session.commit()
        session.refresh(question)

        # Reload full question (with updated options)
        session.refresh(question)
        return QuestionDTO.model_validate(question)


@router.delete("/{question_id}")
def delete_question(question_id: int):
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        session.delete(question)
        session.commit()
    return {"message": "Question deleted successfully"}

@router.get("/all/", response_model=list[QuestionDTO])
def get_all_questions():
    with Session(engine) as session:
        questions = session.query(Question).all()
        return [QuestionDTO.model_validate(question) for question in questions]
