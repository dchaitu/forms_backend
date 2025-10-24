from typing import Optional
from pydantic import BaseModel, ConfigDict
from enums import QuestionType


class UserCreate(BaseModel):
    username: str
    fullname: str
    email_address: str
    password: str

class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    fullname: str
    email_address: str

class FormCreate(BaseModel):
    title: str
    description: str
    created_by: int = 1
    # questions: list[int]

class FormDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    response_link: Optional[str] = None

class FormCompleteDTO(FormCreate):
    form_id: int

class FormDetailsDTO(BaseModel):
    # form_id: int
    title: Optional[str] = None
    description: Optional[str] = None

class SectionCreate(BaseModel):
    title: str
    description: str
    form_id: int

class SectionDTO(SectionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SectionUpdate(BaseModel):
    section_id: int
    title: Optional[str]
    description: Optional[str]

class OptionCreate(BaseModel):
    text: str
    question_id: int

class OptionDTO(OptionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class QuestionCreate(BaseModel):
    section_id: int
    question_type: QuestionType
    title: str
    description: Optional[str]
    is_required: bool
    options: Optional[list[OptionDTO]] = None

class QuestionDTO(QuestionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int



class OptionUpdate(BaseModel):
    id: Optional[int] = None
    text: str

class QuestionUpdate(BaseModel):
    section_id: int
    question_type: QuestionType
    title: str
    description: Optional[str]
    is_required: bool
    options: Optional[list[OptionUpdate]] = None

class SectionCompleteDetailsDTO(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    questions: list[QuestionDTO] = []
    form_id: int
    model_config = ConfigDict(from_attributes=True)

class FormCompleteDetailsDTO(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    sections: list[SectionCompleteDetailsDTO] = []
    response_link: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    form_id: int
    response_data: str