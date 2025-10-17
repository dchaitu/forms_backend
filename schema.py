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
    pass


class QuestionCreate(BaseModel):
    question_type: QuestionType
    form_id: int
    text: str
    option_ids: list[int]

class QuestionDTO(QuestionCreate):
    pass