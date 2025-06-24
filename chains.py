import datetime
from typing import List, Union

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from schemas import ExtractedAnswer, OutputAnswer

load_dotenv()


# === Model + parser ===
llm = ChatOpenAI(model="o4-mini")
parser_pydantic = PydanticToolsParser(tools=[ExtractedAnswer])

# === Prompt template ===
question_extractor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert user survey agent.
Current time: {time}

1. Question: {question}
2. Instructions: {question_instruction}
3. Try to understand user's response and extract information from it.
4. Extract information from user's response in the required format.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

# === Chain definition ===
question_extractor_prompt_template = question_extractor_prompt_template.partial(
    question="How old are you?",
    question_instruction="Try to extract age from user's response. If you don't find age, return 'None'. Age must be a number.",
)

question_extractor = question_extractor_prompt_template | llm.bind_tools(
    tools=[ExtractedAnswer], tool_choice="ExtractedAnswer"
)


summary_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert summary agent.

Instructions: 
1. You can return information about validation failed.
2. You can return information about answer saved.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer using the required format."),
    ]
)

revisor = summary_prompt_template | llm.bind_tools(
    tools=[OutputAnswer], tool_choice="OutputAnswer"
)

# === Example run ===
if __name__ == "__main__":
    chat_history = []

    chain = (
        question_extractor_prompt_template
        | llm.bind_tools(tools=[ExtractedAnswer], tool_choice="ExtractedAnswer")
        | parser_pydantic
    )

    # human_message = HumanMessage(
    #     content="What range of age do you want to answer?")
    # human_message = HumanMessage(
    #     content="I am 21 years old")
    human_message = HumanMessage(content="I am 131 years old")
    chat_history.append(human_message)
    res1 = chain.invoke(input={"messages": chat_history})
    chat_history.append(AIMessage(content=str(res1[0])))
    print("✅ 1st result:", res1)

    # human_message2 = HumanMessage(content="I'm two years older")
    # chat_history.append(human_message2)
    # res2 = first_responder.invoke(input={"messages": chat_history})
    # print("✅ 2nd result:", res2)
