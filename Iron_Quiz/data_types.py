from enum import Enum, auto


class QuizStatus(Enum):
    NO_QUESTION = auto()
    USER_CAN_BOOK = auto()
    USER_WAITING_ALLOWANCE_TO_ANSWER = auto()
    USER_CAN_ANSWER = auto()
    USER_WAITING_VALIDATION = auto()
    USER_WON = auto()
    USER_LOST = auto()
