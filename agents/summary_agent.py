from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.prompt import SUMMARY_PROMPT
from parser.formatter import format_summary
from parser.output_parsers import survey_summary_parser
from Config import Config


def create_survey_summary_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SUMMARY_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, [], prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=[], verbose=Config().show_logs)
    return agent_executor


def process_survey_summary(agent, db, user_input):
    summary = format_summary(db)
    prompt = f"{summary}\n\n{user_input}"
    result = agent.invoke(
        {
            "input": prompt,
            "summary": summary,
            "format_instructions": survey_summary_parser.get_format_instructions()
        })
    return result["output"]
