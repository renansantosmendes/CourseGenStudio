import sys
import logging

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from deep_agent.state import AgentState

logger = logging.getLogger(__name__)

CATEGORIES = "tecnologia, saude, financas ou geral"


class UserContext(BaseModel):
    user_name: str = "User"
    tone: str = "casual"
    language: str = "pt-br"


class DeepAgent:
    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0,
        user_context: UserContext | None = None,
        streaming: bool = True,
    ) -> None:
        self.context = user_context or UserContext()
        self.streaming = streaming
        self._llm = ChatOpenAI(model=model, temperature=temperature)
        logger.info("Initializing DeepAgent (model=%s, streaming=%s)", model, streaming)
        self._graph = self._build_graph()

    # ── Nós ────────────────────────────────────────────────────────

    def _classify_node(self, state: AgentState) -> dict:
        logger.info("Node [classify] started")
        self._print_header("🏷️  CLASSIFICANDO pergunta...")

        result = self._llm.invoke([
            SystemMessage(content=f"Classifique a pergunta em UMA palavra: {CATEGORIES}."),
            HumanMessage(content=state.user_input),
        ])
        category = result.content.strip().lower()
        print(f"   → Categoria: '{category}'", flush=True)
        logger.info("Node [classify] completed — category: '%s'", category)

        return {
            "category": category,
            "thinking": [f"🏷️ Classificação: '{category}'"],
        }

    def _reason_node(self, state: AgentState) -> dict:
        logger.info("Node [reason] started — category: '%s'", state.category)
        self._print_header("🧠  RACIOCINANDO... (streaming token a token)")

        messages = [
            SystemMessage(content=(
                f"Você é um assistente especializado em {state.category}.\n"
                f"Contexto do usuário: {self.context.model_dump()}\n\n"
                "Antes de responder, pense passo a passo sobre a pergunta. "
                "Escreva APENAS seu raciocínio interno, não a resposta final."
            )),
            HumanMessage(content=state.user_input),
        ]

        full_content = self._stream_or_invoke(messages)
        logger.info("Node [reason] completed")

        return {
            "thinking": [f"🧠 Raciocínio:\n{full_content}"],
        }

    def _respond_node(self, state: AgentState) -> dict:
        logger.info("Node [respond] started")
        self._print_header("✍️   GERANDO RESPOSTA... (streaming token a token)")

        reasoning = "\n".join(state.thinking)
        messages = [
            SystemMessage(content=(
                f"Você é um assistente com tom {self.context.tone} para {self.context.user_name}.\n"
                f"Categoria: {state.category}\n\n"
                f"Seu raciocínio prévio:\n{reasoning}\n\n"
                "Agora escreva a resposta final para o usuário, "
                "clara e bem estruturada, baseada no seu raciocínio."
            )),
            HumanMessage(content=state.user_input),
        ]

        full_response = self._stream_or_invoke(messages)
        logger.info("Node [respond] completed")

        return {
            "response": full_response,
            "thinking": ["✅ Resposta gerada com sucesso"],
        }

    # ── Helpers ────────────────────────────────────────────────────

    def _stream_or_invoke(self, messages: list) -> str:
        if self.streaming:
            full_content = ""
            for chunk in self._llm.stream(messages):
                token = chunk.content
                print(token, end="", flush=True)
                full_content += token
            print()
            return full_content
        else:
            result = self._llm.invoke(messages)
            print(result.content, flush=True)
            return result.content

    @staticmethod
    def _print_header(title: str) -> None:
        print(f"\n{'─' * 55}")
        print(title)
        print("─" * 55, flush=True)

    # ── Grafo ──────────────────────────────────────────────────────

    def _build_graph(self) -> CompiledStateGraph:
        logger.debug("Building DeepAgent graph")
        graph = StateGraph(AgentState)

        graph.add_node("classify", self._classify_node)
        graph.add_node("reason", self._reason_node)
        graph.add_node("respond", self._respond_node)

        graph.add_edge(START, "classify")
        graph.add_edge("classify", "reason")
        graph.add_edge("reason", "respond")
        graph.add_edge("respond", END)

        compiled = graph.compile()
        logger.debug("DeepAgent graph compiled successfully")
        return compiled

    def get_graph(self) -> CompiledStateGraph:
        return self._graph

    # ── Interface pública ──────────────────────────────────────────

    def invoke(self, user_input: str) -> AgentState:
        logger.info("DeepAgent invoked — input: '%s'", user_input[:80])
        print("=" * 55)
        print("🤖 AGENTE INICIADO")
        print("=" * 55, flush=True)

        result = self._graph.invoke({"user_input": user_input})

        print(f"\n{'=' * 55}")
        print("✅ PIPELINE COMPLETO")
        print("=" * 55, flush=True)
        logger.info("DeepAgent finished")
        return result
