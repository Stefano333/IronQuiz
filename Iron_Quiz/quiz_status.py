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
    ciao = "a"

    def __init__(self):
        self.status = QuizStatus.NO_QUESTION
    
    def get_status(self, question: dict, booked_answer=False, can_answer=False, 
                    did_answer=False, checked_answer=False, did_win=False, question_id=0):
        self.question = question
        self.booked_answer, self.can_answer = booked_answer, can_answer
        self.did_answer, self.checked_answer = did_answer, checked_answer
        self.did_win, self.id = did_win, id

        if not question:
            self.status = QuizStatus.NO_QUESTION

        elif not booked_answer:
            self.status = QuizStatus.USER_CAN_BOOK

        elif self.booked_answer and not self.can_answer:
            self.status = QuizStatus.USER_WAITING_ALLOWANCE_TO_ANSWER
        
        elif self.can_answer and not self.did_answer:
            self.status = QuizStatus.USER_CAN_ANSWER

        elif self.did_answer and not self.checked_answer:
            self.status = QuizStatus.USER_WAITING_VALIDATION
        
        elif self.checked_answer and not self.did_win:
            self.status = QuizStatus.USER_LOST
        
        elif self.checked_answer and self.did_win:
            self.status = QuizStatus.USER_WON
        
        return self.status

