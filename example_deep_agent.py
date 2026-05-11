from dotenv import load_dotenv
from deep_agent import DeepAgent, UserContext

load_dotenv()

context = UserContext(user_name="Ana", tone="formal", language="pt-br")

agent = DeepAgent(model="gpt-4.1-mini", user_context=context, streaming=True)

questions = [
    "Como funciona a inteligência artificial?",
    "Quais alimentos ajudam a reduzir o colesterol?",
    "Como montar uma reserva de emergência?",
]

for question in questions:
    print(f"\n{'=' * 55}")
    print(f"❓ Pergunta: {question}")
    print("=" * 55)
    agent.invoke(question)
    input("\nPressione Enter para a próxima pergunta...")
