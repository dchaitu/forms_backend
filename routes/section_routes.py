from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from models import engine, Section, Question
from schema import SectionCreate, SectionDTO, SectionUpdate, QuestionDTO, SectionCompleteDetailsDTO

router = APIRouter(prefix='/section', tags=['Section'])

@router.post("/create/", response_model=SectionDTO)
def create_section(section_create: SectionCreate):
    with Session(engine) as session:
        db_section = Section(**section_create.model_dump())
        session.add(db_section)
        section_dto = SectionDTO.model_validate(db_section)
        session.commit()
        session.refresh(db_section)

        return section_dto

@router.post('/add/{question_id}/')
def add_question_to_section(question_id: int, section_id: int):
    with Session(engine) as session:
        section = session.get(Section, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        section.questions.append(question)
        session.commit()
    return {"message": "Question added to section successfully"}

@router.get("/{section_id}", response_model=SectionDTO)
def get_section(section_id: int):
    with Session(engine) as session:
        section = session.get(Section, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        return SectionDTO.model_validate(section)

@router.put("/", response_model=SectionDTO)
def update_section(section_update: SectionUpdate):
    with Session(engine) as session:
        section = session.get(Section, section_update.section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        section.title = section_update.title
        section.description = section_update.description
        section_data = section_update.model_dump(exclude_unset=True)
        for key, value in section_data.items():
            setattr(section, key, value)

        session.add(section)
        session.commit()
        session.refresh(section)
        return SectionDTO.model_validate(section)

@router.delete("/{section_id}")
def delete_section(section_id: int):
    with Session(engine) as session:
        section = session.get(Section, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
        session.delete(section)
        session.commit()
    return {"message": "Section deleted successfully"}


@router.get("/all/", response_model=list[SectionDTO])
def get_all_sections():
    with Session(engine) as session:
        sections = session.query(Section).all()
        return [SectionDTO.model_validate(section) for section in sections]


@router.get("/{section_id}/complete/", response_model=SectionCompleteDetailsDTO)
def get_section_questions(section_id: int):
    with Session(engine) as session:
        section = session.get(Section, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        section_dto = SectionCompleteDetailsDTO(
            id=section.id,
            title=section.title,
            description=section.description,
            questions=[QuestionDTO.model_validate(question) for question in section.questions],
            form_id=section.form_id
        )
        return section_dto
