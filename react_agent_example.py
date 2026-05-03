"""
React Agent com LangGraph — Arquitetura Orientada a Objetos
===========================================================
Encapsula toda a lógica do agente em uma classe reutilizável e extensível.

Instalação:
    pip install langgraph langchain-anthropic langchain-core

Uso:
    export ANTHROPIC_API_KEY="sua-chave-aqui"
    python react_agent_class.py
"""

import os
from typing import Annotated, Any, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool, tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph


# ─── ESTADO ───────────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ─── FERRAMENTAS PADRÃO ────────────────────────────────────────────────────────

@tool
def calculator(expression: str) -> str:
    """Avalia uma expressão matemática. Ex: '2 ** 10 + 5 * 3'"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Resultado: {result}"
    except Exception as e:
        return f"Erro: {e}"


@tool
def web_search(query: str) -> str:
    """Simula uma busca na web. Em produção, use Tavily ou SerpAPI."""
    return f"[Busca simulada] Resultado para '{query}': informação fictícia."


@tool
def get_weather(city: str) -> str:
    """Retorna a previsão do tempo para uma cidade."""
    return f"[Clima simulado] {city}: 22°C, parcialmente nublado."


# ─── CLASSE PRINCIPAL ──────────────────────────────────────────────────────────

class ReactAgent:
    """
    Agente ReAct encapsulado em classe, construído sobre LangGraph.

    Responsabilidades:
    - Gerenciar o modelo LLM e as ferramentas disponíveis
    - Construir e compilar o grafo de execução
    - Expor métodos de invocação (single-turn e multi-turn)

    Exemplo de uso:
        agent = ReactAgent(tools=[calculator, web_search])
        response = agent.invoke("Quanto é 2 ** 10?")
        print(response)
    """

    DEFAULT_SYSTEM_PROMPT = (
        "Você é um assistente útil com acesso a ferramentas. "
        "Raciocine passo a passo antes de responder. "
        "Use ferramentas sempre que necessário para dar respostas precisas."
    )

    def __init__(
        self,
        tools: list[BaseTool] | None = None,
        model: str = "claude-3-5-sonnet-20241022",
        system_prompt: str | None = None,
        api_key: str | None = None,
        temperature: float = 0,
        verbose: bool = False,
    ) -> None:
        """
        Args:
            tools:         Lista de ferramentas LangChain (@tool). Usa padrões se None.
            model:         ID do modelo Anthropic.
            system_prompt: Instrução de sistema customizada.
            api_key:       Chave da API (usa ANTHROPIC_API_KEY se None).
            temperature:   Temperatura do modelo (0 = determinístico).
            verbose:       Imprime logs dos nós se True.
        """
        self.tools = tools or [calculator, web_search, get_weather]
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.verbose = verbose

        # Mapeia nome → função para execução no tool_node
        self._tool_map: dict[str, BaseTool] = {t.name: t for t in self.tools}

        # Inicializa o LLM com as ferramentas vinculadas
        self._llm = ChatAnthropic(
            model=model,
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
            temperature=temperature,
        )
        self._llm_with_tools = self._llm.bind_tools(self.tools)

        # Histórico para conversas multi-turn
        self._history: list[BaseMessage] = []

        # Compila o grafo uma única vez na inicialização
        self._graph: CompiledStateGraph = self._build_graph()

    # ── Nós do Grafo ──────────────────────────────────────────────────────────

    def _agent_node(self, state: AgentState) -> AgentState:
        """Raciocina sobre o estado atual e decide a próxima ação."""
        self._log("[agent] Chamando LLM...")

        messages = state["messages"]

        # Injeta system prompt como primeira mensagem, se ainda não estiver lá
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=self.system_prompt)] + list(messages)

        response = self._llm_with_tools.invoke(messages)
        self._log(f"[agent] Resposta: {response.content[:80]}...")
        return {"messages": [response]}

    def _tool_node(self, state: AgentState) -> AgentState:
        """Executa todas as tool_calls da última mensagem do agente."""
        last_message: AIMessage = state["messages"][-1]
        results: list[ToolMessage] = []

        for call in last_message.tool_calls:
            name, args, call_id = call["name"], call["args"], call["id"]
            self._log(f"[tools] Executando '{name}' | args={args}")

            if name in self._tool_map:
                output = self._tool_map[name].invoke(args)
            else:
                output = f"Erro: ferramenta '{name}' não encontrada."

            results.append(ToolMessage(content=str(output), tool_call_id=call_id, name=name))

        return {"messages": results}

    # ── Roteamento ────────────────────────────────────────────────────────────

    def _should_continue(self, state: AgentState) -> str:
        """Roteador: 'tools' se há tool_calls pendentes, 'end' caso contrário."""
        last: AIMessage = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else "end"

    # ── Construção do Grafo ───────────────────────────────────────────────────

    def _build_graph(self) -> CompiledStateGraph:
        """Monta e compila o StateGraph do agente."""
        graph = StateGraph(AgentState)

        graph.add_node("agent", self._agent_node)
        graph.add_node("tools", self._tool_node)

        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent",
            self._should_continue,
            {"tools": "tools", "end": END},
        )
        graph.add_edge("tools", "agent")

        return graph.compile()

    # ── Interface Pública ─────────────────────────────────────────────────────

    def invoke(self, user_input: str) -> str:
        """
        Executa o agente em modo single-turn (sem histórico).

        Args:
            user_input: Mensagem do usuário.

        Returns:
            Resposta final do agente como string.
        """
        state = self._graph.invoke({"messages": [HumanMessage(content=user_input)]})
        return state["messages"][-1].content

    def chat(self, user_input: str) -> str:
        """
        Executa o agente em modo multi-turn (mantém histórico de conversa).

        Args:
            user_input: Mensagem do usuário.

        Returns:
            Resposta final do agente como string.
        """
        self._history.append(HumanMessage(content=user_input))
        state = self._graph.invoke({"messages": self._history})

        # Atualiza o histórico com todas as mensagens geradas neste turno
        self._history = state["messages"]
        return self._history[-1].content

    def reset(self) -> None:
        """Limpa o histórico de conversa."""
        self._history = []
        self._log("[agent] Histórico resetado.")

    def add_tool(self, new_tool: BaseTool) -> None:
        """
        Adiciona uma ferramenta dinamicamente e reconstrói o grafo.

        Args:
            new_tool: Ferramenta LangChain decorada com @tool.
        """
        self.tools.append(new_tool)
        self._tool_map[new_tool.name] = new_tool
        self._llm_with_tools = self._llm.bind_tools(self.tools)
        self._graph = self._build_graph()
        self._log(f"[agent] Ferramenta '{new_tool.name}' adicionada.")

    def stream(self, user_input: str):
        """
        Itera sobre os passos intermediários do agente (streaming de nós).

        Yields:
            dict com o estado após cada nó executado.
        """
        for step in self._graph.stream({"messages": [HumanMessage(content=user_input)]}):
            yield step

    @property
    def tool_names(self) -> list[str]:
        """Retorna os nomes das ferramentas registradas."""
        return list(self._tool_map.keys())

    # ── Utilitários ───────────────────────────────────────────────────────────

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def __repr__(self) -> str:
        return (
            f"ReactAgent(tools={self.tool_names}, "
            f"history_len={len(self._history)})"
        )


# ─── EXEMPLO DE SUBCLASSE (extensão) ──────────────────────────────────────────

class ResearchAgent(ReactAgent):
    """
    Especialização do ReactAgent para pesquisa.
    Demonstra como estender a classe base com comportamento customizado.
    """

    DEFAULT_SYSTEM_PROMPT = (
        "Você é um agente de pesquisa especializado. "
        "Sempre cite fontes, organize respostas com tópicos claros "
        "e prefira dados quantitativos quando disponíveis."
    )

    def invoke(self, user_input: str) -> str:
        """Adiciona prefixo de pesquisa antes de invocar."""
        enriched = f"Pesquise e responda com detalhes: {user_input}"
        return super().invoke(enriched)


# ─── DEMONSTRAÇÃO ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── 1. Uso básico ──────────────────────────────────────────────────────
    print("=" * 60)
    print("1. USO BÁSICO (single-turn)")
    print("=" * 60)

    agent = ReactAgent(
        tools=[calculator, web_search, get_weather],
        verbose=True,
    )
    print(repr(agent))

    resposta = agent.invoke("Quanto é (123 * 456) + 789?")
    print(f"\nResposta: {resposta}")

    # ── 2. Conversa multi-turn ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("2. CONVERSA MULTI-TURN")
    print("=" * 60)

    r1 = agent.chat("Olá! Qual é o clima em Recife?")
    print(f"Turno 1: {r1}")

    r2 = agent.chat("E em São Paulo?")
    print(f"Turno 2: {r2}")

    r3 = agent.chat("Qual cidade está mais quente?")
    print(f"Turno 3: {r3}")

    # ── 3. Adicionando ferramenta dinamicamente ────────────────────────────
    print("\n" + "=" * 60)
    print("3. ADICIONANDO FERRAMENTA DINAMICAMENTE")
    print("=" * 60)

    @tool
    def get_stock_price(ticker: str) -> str:
        """Retorna o preço simulado de uma ação. Ex: 'PETR4'"""
        prices = {"PETR4": "R$ 38,50", "VALE3": "R$ 62,10", "ITUB4": "R$ 34,90"}
        return prices.get(ticker.upper(), f"Ticker '{ticker}' não encontrado.")

    agent.add_tool(get_stock_price)
    print(f"Ferramentas agora: {agent.tool_names}")

    r4 = agent.invoke("Qual o preço da VALE3?")
    print(f"Resposta: {r4}")

    # ── 4. Streaming de passos ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("4. STREAMING DE PASSOS INTERMEDIÁRIOS")
    print("=" * 60)

    for step in agent.stream("Quanto é 2 ** 20?"):
        node_name = list(step.keys())[0]
        print(f"  → Nó executado: {node_name}")

    # ── 5. Subclasse especializada ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("5. SUBCLASSE ResearchAgent")
    print("=" * 60)

    research = ResearchAgent(tools=[web_search], verbose=False)
    r5 = research.invoke("LangGraph e suas vantagens")
    print(f"Resposta: {r5}")
  
