from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(..., description="The generated question")
    answer: str | None = Field(
        None, description="The answer to the question, if available"
    )
    
    
class Choice(BaseModel):
    label: str = Field(..., description="Label of the alternative (e.g., A, B, C, D)")
    text: str = Field(..., description="Text of the alternative")
    is_correct: bool = Field(..., description="Indicates if this alternative is correct")
    explanation: str | None = Field(
        None, description="Explanation for why this alternative is correct or incorrect"
    )

class MultipleChoiceQuestion(Question):
    alternatives: list[Choice] = Field(..., description="List of alternatives for the question")
    correct_alternative: str = Field(..., description="The correct alternative")
