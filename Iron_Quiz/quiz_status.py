from enum import Enum, auto


class QuizStatus(Enum):
    NO_QUESTION = auto()
    USER_CAN_BOOK = auto()
    USER_WAITING_ALLOWANCE_TO_ANSWER = auto()
    USER_CAN_ANSWER = auto()
    USER_WAITING_VALIDATION = auto()
    USER_WON = auto()
    USER_LOST = auto()

class Quiz():
    def __init__(self):
        self._status = QuizStatus.NO_QUESTION

    def get_status(self, question: dict, booked_answer=False, can_answer=False, 
                    did_answer=False, checked_answer=False, did_win=False, question_id=0):
        self._question = question
        self._booked_answer, self._can_answer = booked_answer, can_answer
        self._did_answer, self._checked_answer = did_answer, checked_answer
        self._did_win, self._id = did_win, id

        if not booked_answer:
            self._status = QuizStatus.USER_CAN_BOOK

        elif self._booked_answer and not self._can_answer:
            self._status = QuizStatus.USER_WAITING_ALLOWANCE_TO_ANSWER
        
        elif self._can_answer and not self._did_answer:
            self._status = QuizStatus.USER_CAN_ANSWER

        elif self._did_answer and not self._checked_answer:
            self._status = QuizStatus.USER_WAITING_VALIDATION
        
        elif self._checked_answer and not self._did_win:
            self._status = QuizStatus.USER_LOST
        
        elif self._checked_answer and self._did_win:
            self._status = QuizStatus.USER_WON
        
        return self._status