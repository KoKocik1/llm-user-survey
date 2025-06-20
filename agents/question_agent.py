from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.tools import Tools
from utils.prompt import SYSTEM_PROMPT
from parser.output_parsers import survey_response_parser
from questions.questions import Questions
from Config import Config


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
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=Config().show_logs)

    return agent_executor


def process_survey_question(agent, question: str, user_input: str) -> str:
    """Process a single survey question with user input."""
    prompt = f"Question: {question}\nUser input: {user_input}\n\nProcess this response according to the question type and save to database."

    try:
        result = agent.invoke(
            {
                "input": prompt,
                "instructions": Questions.question_tool(question),
                "database": Questions.MOCK_DB,
                "format_instructions": survey_response_parser.get_format_instructions()
            })
        return result["output"]
    except Exception as e:
        return f"Error processing question: {str(e)}"
