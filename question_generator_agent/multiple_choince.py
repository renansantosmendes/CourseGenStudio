import os
import uuid
from typing import TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph

from question_generator_agent.prompts import QUESTION_GENERATION_PROMPT
from question_generator_agent.models import MultipleChoiceQuestion

from dotenv import load_dotenv

load_dotenv()

class QuestionInput(TypedDict):
    subject_name: str
    subject_content: str
    question_topic: str
    question_type: str
    level: str


class MultipleChoiceQuestionGeneratorAgent:
    def __init__(
        self,
        model: str = "gpt-4.1-nano",
        system_prompt: str | None = None,
        api_key: str | None = None,
        temperature: float = 0,
        verbose: bool = False,
        subject_content: str | None = None,
        subject_name: str | None = None,
    ) -> None:

        self.system_prompt = system_prompt or QUESTION_GENERATION_PROMPT
        self.verbose = verbose
        self.subject_content = subject_content
        self.subject_name = subject_name

        _llm = ChatOpenAI(
            model=model,
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            temperature=temperature,
        ).with_structured_output(MultipleChoiceQuestion)

        _prompt = ChatPromptTemplate.from_template(self.system_prompt)

        self._chain: Runnable = _prompt | _llm

        self._checkpointer = MemorySaver()
        self._thread_id: str = str(uuid.uuid4())

        self._attempts = 0

    def _build_input(self, question_topic: str, level: str) -> QuestionInput:
        return QuestionInput(
            subject_name=self.subject_name or "",
            subject_content=self.subject_content or "",
            question_topic=question_topic,
            question_type="múltipla escolha",
            level=level,
        )

    def _build_graph(self) -> CompiledStateGraph:
        ...

    def invoke(self, question_input: dict) -> MultipleChoiceQuestion:
        full_input = self._build_input(**question_input)
        return self._chain.invoke(full_input)
