from pydantic import BaseModel, Field
from enum import Enum


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


class CriterionStatus(str, Enum):
    APPROVED = "aprovado"
    WARNING = "atenção"
    REJECTED = "reprovado"


class Severity(str, Enum):
    LOW = "baixa"
    MEDIUM = "média"
    HIGH = "alta"


class GlobalStatus(str, Enum):
    APPROVED = "aprovada"
    APPROVED_WITH_CAVEATS = "aprovada com ressalvas"
    REJECTED = "reprovada"


class CriterionEvaluation(BaseModel):
    """Avaliação de um critério individual de qualidade."""
    criterion_name: str = Field(
        description="Nome do critério avaliado"
    )
    status: CriterionStatus = Field(
        description="Status do critério: aprovado, atenção ou reprovado"
    )
    observation: str = Field(
        description="Comentário objetivo sobre o que foi identificado neste critério"
    )


class Issue(BaseModel):
    """Problema detectado na questão com sugestão de correção."""
    description: str = Field(
        description="Descrição objetiva do problema encontrado"
    )
    criterion_name: str = Field(
        description="Nome do critério de qualidade afetado por este problema"
    )
    severity: Severity = Field(
        description="Severidade do problema: baixa, média ou alta"
    )
    problematic_excerpt: str = Field(
        description="Trecho literal da questão onde o problema foi identificado"
    )
    suggestion: str = Field(
        description="Proposta concreta de como corrigir o problema"
    )


class QuestionQualityEvaluation(BaseModel):
    """Resultado completo da avaliação de qualidade de uma questão."""
    global_status: GlobalStatus = Field(
        description="Status global da questão: aprovada, aprovada com ressalvas ou reprovada"
    )
    criteria: list[CriterionEvaluation] = Field(
        description="Avaliação individual de cada um dos 8 critérios de qualidade"
    )
    issues: list[Issue] = Field(
        default_factory=list,
        description=(
            "Lista de problemas encontrados com sugestões de correção. "
            "Vazia se todos os critérios forem aprovados."
        )
    )
