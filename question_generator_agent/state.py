from typing import TypedDict, Optional
from question_generator_agent.models import MultipleChoiceQuestion, QuestionQualityEvaluation

class QuestionCreationState(TypedDict):
    subject_name: str
    subject_content: str
    question_topic: str
    question_type: str
    level: str
    generated_question: Optional[MultipleChoiceQuestion]
    evaluation: Optional[QuestionQualityEvaluation]
    corrected_question: Optional[MultipleChoiceQuestion]

    attempts: int
