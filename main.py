import datetime
import re
from typing import Union, Dict, Any
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

act_year = datetime.date.today().year
QUESTION_INSTRUCTION = {
    "Jaka jest twoja waga w kg?": "Wyciagnij z odpowiedzi wage pomiedzy 10 a 200 kg i zwroc ja jako liczbe calkowita.",
    "Jaki jest Twoj rok urodzenia?": f"Znajdz 4-cyfrowa liczbe w przedziale [{act_year-100}, {act_year}] i zwroc ja jako liczbe calkowita.",
    "Jaka jest twoja płeć?": "Normalizuj odpowiedz do jednej z trzech wartosci: 'M' dla Mezczyzny, 'K' dla Kobiety",
    "Czy masz alergie? Jezeli tak to je wymień.": "Jeśli użytkownik odpowie, ze nie ma, zwróć nie. W przeciwnym razie wyciagnij alergie rozdzielone przecinkami"
}
MOCK_DB = {
    "waga": None,
    "rok_urodzenia": None,
    "plec": None,
    "alergie": None
}

QUESTION_TO_DB_KEY = {
    "Jaka jest twoja waga w kg?": "waga",
    "Jaki jest Twoj rok urodzenia?": "rok_urodzenia",
    "Jaka jest twoja płeć?": "plec",
    "Czy masz alergie? Jezeli tak to je wymień.": "alergie"
}


@tool
def validate_range(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]) -> bool:
    """Validates if a value is within the specified range."""
    return min_value <= value <= max_value


@tool
def save_to_database(question: str, answer: Any) -> str:
    """Saves the answer to the mock database for the given question."""
    db_key = QUESTION_TO_DB_KEY.get(question)
    if db_key:
        MOCK_DB[db_key] = answer
        return f"OK - Saved {answer} to {db_key}"
    return "Error - Question not found in database mapping"


# @tool
# def get_question_instruction(question: str) -> str:
#     """Gets the specific instruction for processing a question."""
#     return QUESTION_INSTRUCTION.get(question, "No instruction found for the given question.")


def create_survey_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [
        validate_range,
        save_to_database,
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a survey agent that processes user responses to questions. Your task is to:

1. Extract the relevant information from user input based on the question type
2. Validate the extracted value if it has a range requirement
3. Save the answer to the database
4. Return appropriate responses

For each question, you should:
- Use the appropriate extraction tool based on the question type
- Validate ranges when applicable using validate_range tool
- Save the result using save_to_database tool
- Return "OK" if successful, inform user that you can't understand and ask question again if you can't understand, or inform user that validation failed and ask question again

Question type and its processing:
{instructions}


Always be helpful and ask for clarification if needed."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


def process_survey_question(agent, question: str, user_input: str) -> str:
    """Process a single survey question with user input."""
    prompt = f"Question: {question}\nUser input: {user_input}\n\nProcess this response according to the question type and save to database."

    try:
        result = agent.invoke(
            {"input": prompt, "instructions": question_tool(question)})
        return result["output"]
    except Exception as e:
        return f"Error processing question: {str(e)}"


def question_tool(question: str) -> str:
    return QUESTION_INSTRUCTION.get(question, "No instruction found for the given question.")


def get_all_questions():
    return "\n".join(list(QUESTION_INSTRUCTION.keys()))


if __name__ == "__main__":
    print(
        f"Czesc! Oto pytania, ktore musisz odpowiedziec:\n{get_all_questions()}\n Zaczynajmy!")

    agent = create_survey_agent()

    for question in QUESTION_INSTRUCTION.keys():
        print(f"\n{question}\n")
        while True:
            user_input = input()
            result = process_survey_question(agent, question, user_input)
            print(f"Result: {result}")
            if result == "OK":
                break

    print(f"\nFinal database state: {MOCK_DB}")
