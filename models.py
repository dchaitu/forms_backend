from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Integer, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import sqlalchemy as sa

from enums import QuestionType


engine = sa.create_engine("sqlite:///forms.db") # Creates db

 # Defining Base for ORM models
# metadata = sa.MetaData()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    email_address: Mapped[str] = mapped_column(String)
    pic_url: Mapped[str] = mapped_column(String)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    forms = relationship("Form", back_populates="user")

    def __str__(self):
        return f"{self.username} {self.fullname}"


class Form(Base):
    __tablename__ = "Form"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]  = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("User.user_id"))
    sections: Mapped[list["Section"]] = relationship(back_populates="form", cascade="all, delete")
    user: Mapped["User"] = relationship(back_populates="forms")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    form_image: Mapped[str] = mapped_column(String)

class Section(Base):
    __tablename__ = "Section"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, default="Untitled Section")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("Form.id"))
    order: Mapped[int] = mapped_column(Integer, default=0)
    # section_image: Mapped[str] = mapped_column(String)
    form: Mapped["Form"] = relationship(back_populates="sections")
    questions: Mapped[list["Question"]] = relationship(back_populates="section", cascade="all, delete")


class Question(Base):
    __tablename__ = "Question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_type: Mapped[QuestionType] = mapped_column(String)
    section_id: Mapped[int] = mapped_column(ForeignKey("Section.id"))
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    options: Mapped[list["Option"]] = relationship(back_populates="question", cascade="all, delete")
    section: Mapped["Section"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="question")
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    question_image: Mapped[str] = mapped_column(String)

class Option(Base):
    __tablename__ = "Option"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("Question.id"))
    text: Mapped[str] = mapped_column(String)
    question: Mapped["Question"] = relationship(back_populates="options")
    answers: Mapped[list["Answer"]] = relationship(back_populates="option", cascade="all, delete")
    option_image: Mapped[str] = mapped_column(String)

class Response(Base):
    __tablename__ = "Response"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("Form.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"))
    answers: Mapped[list["Answer"]] = relationship(back_populates="response", cascade="all, delete")
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class Answer(Base):
    __tablename__ = "Answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("Response.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("Question.id"))
    text: Mapped[str] = mapped_column(String)
    option_id: Mapped[int] = mapped_column(ForeignKey("Option.id"), nullable=True)

    response: Mapped["Response"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship(back_populates="answers")
    option: Mapped["Option"] = relationship(back_populates="answers")

def create_tables():
    Base.metadata.create_all(engine)


with Session(engine) as session:
    # chaitu = User(username="chaitu", fullname="Chaitanya", email_address="chaitu@gmail.com", last_login=datetime.now())
    # lokesh = User(username="lokesh", fullname="Lokesh", email_address="lokesh@gmail.com", last_login=datetime.now())
    # session.add(chaitu)
    session.commit()