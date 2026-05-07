from question_generator_agent.multiple_choince import MultipleChoiceQuestionGeneratorAgent
from question_generator_agent.subject_content import SLIDES_CONTENT

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    agent = MultipleChoiceQuestionGeneratorAgent(
        subject_content=SLIDES_CONTENT,
        subject_name="Generative AI e Advanced Analytics",
    )

    question = agent.invoke({
        "question_topic": "Autoencoders Variacionais",
        "level": "difícil",
    })
    
    print(question)