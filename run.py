import logging
from question_generator_agent.multiple_choince import MultipleChoiceQuestionGeneratorAgent
from question_generator_agent.subject_content import SLIDES_CONTENT
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")

load_dotenv()

if __name__ == "__main__":
    agent = MultipleChoiceQuestionGeneratorAgent(
        subject_content=SLIDES_CONTENT,
        subject_name="Generative AI e Advanced Analytics",
        verbose=True
        )

    agent.get_graph()

    question = agent.invoke(
        {
            "question_topic": "Redes Neurais Generativas Adversariais (GANs)",
            "level": "dificil",
        }
    )
    print("Generated Question:", question)