from typing import Optional

from pydantic import BaseModel

from enums import QuestionType


class UserCreate(BaseModel):
    username: str
    fullname: str
    email_address: str

class UserDTO(UserCreate):
    pass

class FormCreate(BaseModel):
    title: str
    description: str
    created_by: int
    questions: list[int]

class FormDTO(FormCreate):
    form_id: int

class FormDetailsDTO(BaseModel):
    form_id: int
    title: str
    description: str

class SectionCreate(BaseModel):
    title: str
    description: str
    form_id: int

class SectionDTO(SectionCreate):
    section_id: int

class SectionUpdate(BaseModel):
    section_id: int
    title: Optional[str]
    description: Optional[str]

class QuestionCreate(BaseModel):
    section_id: int
    question_type: QuestionType
    title: str
    description: Optional[str]
    option_ids: list[int]

class QuestionDTO(QuestionCreate):
    question_id: int

class OptionCreate(BaseModel):
    text: str
    question_id: int

class OptionDTO(OptionCreate):
    option_id: int

class OptionUpdate(BaseModel):
    text: Optional[str]
    option_id: Optional[int]
