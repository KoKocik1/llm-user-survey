from typing import List

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from chains import question_extractor, revisor
from tool_executor import execute_tools

MAX_ITERATIONS = 2
builder = MessageGraph()
builder.add_node("extractor", question_extractor)
builder.add_node("execute_tools", execute_tools)
builder.add_node("recap", revisor)
builder.add_edge("extractor", "execute_tools")
builder.add_edge("execute_tools", "recap")
builder.add_edge("recap", END)


# def event_loop(state: List[BaseMessage]) -> str:
#     count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
#     num_iterations = count_tool_visits
#     if num_iterations > MAX_ITERATIONS:
#         return END
#     return "execute_tools"


# builder.add_conditional_edges(
#     "revise", event_loop, {END: END, "execute_tools": "execute_tools"})
builder.set_entry_point("extractor")
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


res = graph.invoke("I am 210 years old")
print("Output message:", res[-1].tool_calls[0]["args"]["message"])

# print(res)
