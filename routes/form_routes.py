from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Form, engine, Section
from schema import FormCreate, FormDTO, FormDetailsDTO

router = APIRouter(prefix='/form', tags=['Form'])


@router.post("/create/", response_model=FormDTO)
def create_form(form_create: FormCreate):
    with Session(engine) as session:
        db_form = Form(**form_create.model_dump())
        session.add(db_form)
        session.commit()
        session.refresh(db_form)
        return db_form

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
        return form


@router.get("/all/", response_model=list[FormDTO])
def get_all_forms():
    with Session(engine) as session:
        query = select(Form)
        forms = session.scalars(query).all()
        return forms

@router.get("/{form_id}", response_model=FormDetailsDTO)
def get_form(form_id: int):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return form

@router.delete("/{form_id}")
def delete_form(form_id: int):
    with Session(engine) as session:
        form = session.get(Form, form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        session.delete(form)
        session.commit()
    return {"message": "Form deleted successfully"}