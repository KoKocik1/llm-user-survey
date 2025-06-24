from typing import Union

from dotenv import load_dotenv
from langchain_core.tools import StructuredTool, tool
from langgraph.prebuilt import ToolNode

from schemas import ExtractedAnswer

load_dotenv()

QUESTIONS = {
    "How old are you?": {"instruction": "blablabla", "min_value": 10, "max_value": 120},
}


def validate_range(
    value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]
) -> bool:
    """Sprawdza czy wartość mieści się w określonym zakresie."""
    return min_value <= value <= max_value


def validate_answer(answer: str, question: str) -> bool:
    """Sprawdza czy odpowiedź jest poprawna."""
    question_data = QUESTIONS.get(question)
    if not question_data:
        return True  # nothing to validate
    if validate_range(
        float(answer), question_data["min_value"], question_data["max_value"]
    ):
        return True
    return False


execute_tools = ToolNode(
    [
        StructuredTool.from_function(validate_answer, name=ExtractedAnswer.__name__),
    ]
)
