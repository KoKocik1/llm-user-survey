from typing import Union, Any
from langchain_core.tools import tool
from questions.questions import Questions


@tool
def validate_range(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]) -> bool:
    """Sprawdza czy wartość mieści się w określonym zakresie."""
    return min_value <= value <= max_value


@tool
def save_to_database(question: str, answer: Any) -> str:
    """Zapisuje odpowiedź do bazy danych dla danego pytania."""
    db_key = Questions.get_question_db_key(question)
    if db_key:
        Questions.MOCK_DB[db_key] = answer
        return f"OK - Zapisano {answer} do {db_key}"
    return "Błąd - Nie znaleziono pytania w mapowaniu bazy danych"


class Tools:
    validate_range = validate_range
    save_to_database = save_to_database
