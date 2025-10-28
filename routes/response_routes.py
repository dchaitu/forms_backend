import csv
import json

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from models import engine, Response, Question, Option
from schema import ResponseDTO

router = APIRouter(prefix='/response', tags=['Response'])


# @router.post("/")
# def create_response(response_data: dict):
#     with Session(engine) as session:
#         new_response = Response(response_data=response_data)
#         session.add(new_response)
#         session.commit()
#     return {"message": "Response submitted successfully"}

@router.get("/{form_id}/count")
def get_response_count(form_id: int):
    with Session(engine) as session:
        count = session.query(Response).filter(Response.form_id == form_id).count()
    return {"count": count}


@router.get("/{form_id}/", response_model=list[ResponseDTO])
def get_form_responses(form_id: int):
    with Session(engine) as session:
        responses = session.query(Response).filter(Response.form_id == form_id).all()
        return [ResponseDTO.model_validate(response) for response in responses]


@router.get("/{form_id}/csv")
def get_form_responses_csv(form_id: int):
    with Session(engine) as session:
        responses = session.query(Response).filter(Response.form_id == form_id).all()

        with open('data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["response_id", "user_id", "section_id", "question_id","question_title", "question_description", "answer_description"])
            for response in responses:
                response_info = json.loads(response.response_data)
                for key, val in response_info.items():
                    response_id = response.id
                    user_id = response.user_id
                    question = session.get(Question, key)
                    question_id = question.id
                    section_id = question.section_id
                    question_title = session.get(Question, key).title
                    question_description = session.get(Question, key).description or ""
                    if type(val) == int:
                        answer_description = session.get(Option, val).text
                    elif type(val) == list:
                        answer_description = [session.get(Option, v).text for v in val]
                    else:
                        answer_description = val

                    writer.writerow([response_id, user_id, section_id, question_id, question_title, question_description, answer_description])

    return FileResponse(media_type="text/csv", filename="data_response.csv",path="data.csv")