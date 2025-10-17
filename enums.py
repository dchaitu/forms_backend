from enum import Enum


class QuestionType(Enum):
    TEXT = "text"
    PARAGRAPH = "paragraph"
    DATE = "date"
    TIME = "time"
    MULTIPLE_CHOICE = "multiple_choice"
    CHECKBOXES = "checkboxes"
    DROPDOWN = "dropdown"