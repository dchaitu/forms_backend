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
    text: Optional[str]
    option_id: Optional[int]

class QuestionUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    question_type: Optional[QuestionType]

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
    model_config = ConfigDict(from_attributes=True)