from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def pick_llm(level : str):
    """
        Picks the appropriate LLM absed on the level of the question

        Args:
            level(str) : The level of the question can be 'easy' , 'medium' , 'hard'

        returns:
            str : the LLM to be used:
    """

    normalized = level.strip().lower()

    if normalized == "easy":
        # Fast, lightweight conversational model
        model = "openai/gpt-oss-20b"
    elif normalized == "medium":
        # Balanced 27B model for SQL generation and schema reasoning
        model = "qwen/qwen3.8-27b"
    elif normalized == "hard":
        # Flagship 120B model for deep reasoning / judging
        model = "openai/gpt-oss-20b"
    elif level.lower() == "etl_analyst":
        model = "openai/gpt-oss-20b"
    else:
        raise ValueError("Inavlid level. Choose from 'easy' ,'medium' , 'hard'.")

    llm = ChatGroq(
            model=model,
            temperature=0,
            # model_kwargs={
            #     "reasoning_effort" : None
            # }
        )
    return llm

