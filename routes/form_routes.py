import json
import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models import Form, engine, Section, Question, Response
from schema import FormCreate, FormDTO, FormDetailsDTO, FormCompleteDetailsDTO, SectionCompleteDetailsDTO, QuestionDTO, \
    OptionDTO, ResponseDTO

router = APIRouter(prefix='/form', tags=['Form'])


@router.post("/create/", response_model=FormDTO)
def create_form(form_create: FormCreate):
    with Session(engine) as session:
        db_form = Form(**form_create.model_dump())
        session.add(db_form)
        session.commit()
        session.refresh(db_form)
        default_section = Section(title="Untitled Section", description="", form_id=db_form.id)
        session.add(default_section)
        session.commit()
        session.refresh(db_form)
        return FormDTO.model_validate(db_form)

@router.post("/add/{section_id}/")
def add_section_to_form(section_id: int, form_id: int):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        section = session.get(Section, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        
        # Note: A Section is already associated with a Form upon creation via form_id.
        # This endpoint is redundant if a Section cannot be moved between Forms.
        form.sections.append(section)
        session.commit()
    return {"message": "Section added to form successfully"}

@router.put("/{form_id}", response_model=FormDTO)
def update_form_details(form_id: int, form_dto: FormDetailsDTO):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        update_data = form_dto.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(form, key, value)
        session.add(form)
        session.commit()
        session.refresh(form)
        return FormDTO.model_validate(form)


@router.get("/all/", response_model=list[FormDTO])
def get_all_forms():
    with Session(engine) as session:
        query = select(Form)
        forms = session.scalars(query).all()
        return [FormDTO.model_validate(form) for form in forms]

@router.get("/{form_id}", response_model=FormDetailsDTO)
def get_form(form_id: int):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return FormDetailsDTO.model_validate(form)

@router.delete("/{form_id}")
def delete_form(form_id: int):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        session.delete(form)
        session.commit()
    return {"message": "Form deleted successfully"}

@router.get("/{form_id}/complete/", response_model=FormCompleteDetailsDTO)
def get_form_complete_details(form_id: int):
    with Session(engine) as session:
        form = (
            session.query(Form)
            .options(
                joinedload(Form.sections)
                .joinedload(Section.questions)
                .joinedload(Question.options)
            )
            .filter(Form.id == form_id)
            .first()
        )


        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        sections_dto = []
        for section in form.sections:
            # Build nested question DTOs manually
            questions_dto = []
            for question in section.questions:
                options_dto = [
                    OptionDTO.model_validate(opt) for opt in question.options
                ]
                question_dto = QuestionDTO(
                    id=question.id,
                    section_id=question.section_id,
                    title=question.title,
                    description=question.description,
                    question_type=question.question_type,
                    is_required=question.is_required,
                    options=options_dto,
                )
                questions_dto.append(question_dto)

            section_dto = SectionCompleteDetailsDTO(
                id=section.id,
                title=section.title,
                description=section.description,
                form_id=section.form_id,
                questions=questions_dto,
            )
            sections_dto.append(section_dto)

        return FormCompleteDetailsDTO(
            id=form.id,
            title=form.title,
            description=form.description,
            sections=sections_dto,
            response_link=form.response_link
        )


@router.post("/{form_id}/publish/",response_model=dict)
def publish_form(form_id: int):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")


        unique_id = str(uuid.uuid4())
        response_link = f"/response/{unique_id}/"

        # form.is_published = True
        form.response_link = response_link
        session.add(form)
        session.commit()
        session.refresh(form)
    return {"link": form.response_link}

@router.post("/submit/{unique_id}", response_model=ResponseDTO)
def submit_response(unique_id: str, response_data: dict):
    with Session(engine) as session:
        form = session.query(Form).filter(Form.response_link.like(f"%{unique_id}%")).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")

        new_response = Response(user_id=1, form_id=form.id, response_data=json.dumps(response_data))
        session.add(new_response)
        session.commit()
        return ResponseDTO.model_validate(new_response)


@router.get("/by_uuid/{unique_id}", response_model=FormCompleteDetailsDTO)
def get_form_by_uuid(unique_id: str):
    """
    Retrieves the complete details of a form using the unique ID from its response link.
    This is used to render the form for a user to answer.
    """
    with Session(engine) as session:
        form = (
            session.query(Form)
            .options(
                joinedload(Form.sections)
                .joinedload(Section.questions)
                .joinedload(Question.options)
            )
            .filter(Form.response_link.like(f"%{unique_id}%"))
            .first()
        )

        if not form:
            raise HTTPException(status_code=404, detail="Form not found")


    sections_dto = []
    for section in form.sections:
        questions_dto = []
        for question in section.questions:
            options_dto = [
                OptionDTO.model_validate(opt) for opt in question.options
            ]
            question_dto = QuestionDTO(
                id=question.id,
                section_id=question.section_id,
                title=question.title,
                description=question.description,
                question_type=question.question_type,
                is_required=question.is_required,
                options=options_dto,
            )
            questions_dto.append(question_dto)

        section_dto = SectionCompleteDetailsDTO(
            id=section.id,
            title=section.title,
            description=section.description,
            form_id=section.form_id,
            questions=questions_dto,
        )
        sections_dto.append(section_dto)

    return FormCompleteDetailsDTO(
        id=form.id,
        title=form.title,
        description=form.description,
        sections=sections_dto,
    )
