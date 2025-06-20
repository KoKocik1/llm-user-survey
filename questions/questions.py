import datetime

act_year = datetime.date.today().year

QUESTIONS = {
    "Jaka jest twoja waga w kg?": {
        "instruction": "Wyciagnij z odpowiedzi wage pomiedzy 10 a 200 kg i zwroc ja jako liczbe calkowita.",
        "db_key": "waga",
    },
    "Jaki jest Twoj rok urodzenia?": {
        "instruction": f"Znajdz 4-cyfrowa liczbe w przedziale [{act_year-100}, {act_year}] i zwroc ja jako liczbe calkowita.",
        "db_key": "rok_urodzenia",
    },
    "Jaka jest twoja płeć?": {
        "instruction": "Normalizuj odpowiedz do jednej z trzech wartosci: 'M' dla Mezczyzny, 'K' dla Kobiety",
        "db_key": "plec",
    },
    "Czy masz alergie? Jezeli tak to je wymień.": {
        "instruction": "Jeśli użytkownik odpowie, ze nie ma, zwróć nie. W przeciwnym razie wyciagnij alergie rozdzielone przecinkami",
        "db_key": "alergie",
    }
}

MOCK_DB = {
    "waga": None,
    "rok_urodzenia": None,
    "plec": None,
    "alergie": None
}


def question_tool(question: str) -> str:
    return QUESTIONS.get(question, {}).get("instruction", "Nie znaleziono instrukcji dla podanego pytania.")


def get_all_questions():
    return "\n".join(list(QUESTIONS.keys()))


def get_question_db_key(question: str) -> str:
    return QUESTIONS.get(question, {}).get("db_key", "")


def get_question_range(question: str):
    return QUESTIONS.get(question, {}).get("range")


class Questions:
    QUESTIONS = QUESTIONS
    MOCK_DB = MOCK_DB
    question_tool = question_tool
    get_all_questions = get_all_questions
    get_question_db_key = get_question_db_key
    get_question_range = get_question_range
