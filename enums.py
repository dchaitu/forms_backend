from enum import Enum


class QuestionType(Enum):
    TEXT = "text"
    PARAGRAPH = "paragraph"
    DATE = "date"
    TIME = "time"
    MULTIPLE_CHOICE = "multiple_choice"
    CHECKBOXES = "checkboxes"
    DROPDOWN = "dropdown"
    CHECKBOX_GRID = "checkbox_grid"
    LINEAR_SCALE = "linear_scale"
    FILE_UPLOAD = "file_upload"
    RATING = "rating"
    MULTIPLE_CHOICE_GRID = "multiple_choice_grid"