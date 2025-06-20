from typing import Union, Dict, Any
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from tools import Tools
from questions import Questions
from prompt import SYSTEM_PROMPT

load_dotenv()


def create_survey_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [
        Tools.validate_range,
        Tools.save_to_database,
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
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
            {"input": prompt, "instructions": Questions.question_tool(question)})
        return result["output"]
    except Exception as e:
        return f"Error processing question: {str(e)}"


if __name__ == "__main__":
    print(
        f"Czesc! Oto pytania, ktore musisz odpowiedziec:\n{Questions.get_all_questions()}\n Zaczynajmy!")

    agent = create_survey_agent()

    for question in Questions.QUESTIONS.keys():
        print(f"\n{question}\n")
        while True:
            user_input = input()
            result = process_survey_question(agent, question, user_input)
            print(f"Result: {result}")
            if result == "OK":
                break

    print(f"\nFinal database state: {Questions.MOCK_DB}")
