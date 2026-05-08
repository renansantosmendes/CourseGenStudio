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
    

class CorrectedMultipleChoiceQuestion(MultipleChoiceQuestion):
    """Questão de múltipla escolha corrigida com rastreabilidade.

    Herda todos os campos de MultipleChoiceQuestion e adiciona
    o campo corrections_applied para auditoria.
    """
    corrections_applied: list[str] = Field(
        ...,
        description=(
            "List describing each correction applied, linked to the "
            "original issue. Example: 'Issue: alternative B was "
            "accidentally correct. Fix: replaced with an incorrect "
            "but plausible statement about embeddings.'"
        )
    )


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
    

def serialize_issues(issues: list[Issue]) -> str:
    """Converte a lista de issues do schema avaliativo em string
    formatada para uso como input no prompt de correção."""
    parts = []
    for i, issue in enumerate(issues, start=1):
        parts.append(
            f"Problema {i}:\n"
            f"  Descrição: {issue.description}\n"
            f"  Critério afetado: {issue.criterion_name}\n"
            f"  Severidade: {issue.severity.value}\n"
            f"  Trecho problemático: {issue.problematic_excerpt}\n"
            f"  Sugestão de correção: {issue.suggestion}"
        )
    return "\n\n".join(parts)


def serialize_question(question: MultipleChoiceQuestion) -> str:
    """Converte a questão original em string formatada para uso
    como input no prompt de correção."""
    parts = [
        f"Questão: {question.question}",
        f"\nAlternativas:",
    ]
    for alt in question.alternatives:
        status = "(correta)" if alt.is_correct else "(incorreta)"
        parts.append(f"  {alt.label}) {alt.text} {status}")
        if alt.explanation:
            parts.append(f"     Justificativa: {alt.explanation}")

    parts.append(f"\nGabarito: Alternativa {question.correct_alternative}")

    if question.answer:
        parts.append(f"Resposta: {question.answer}")

    return "\n".join(parts)