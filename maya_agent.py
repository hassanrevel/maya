from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from llms import llm
from tools import tools

memory = MemorySaver()

class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatBot):
    prompt = """
    Your name is Maya. You're a warm, polite hospital receptionist. You help visitors book appointments, check doctor availability, and answer any questions about the hospital — including departments, facilities, services, hours, and more.
    Use tools when appropriate. Never repeat your name unless asked. Be helpful and keep track of what the user wants.
    """

    if isinstance(state["messages"][0], dict):
        state["messages"].insert(0, {"role": "system", "content": prompt})
    else:
        state["messages"].insert(0, HumanMessage(content=prompt))

    llm_with_tools = llm.bind_tools(tools=tools)

    ai_message = llm_with_tools.invoke(state["messages"])

    state["messages"].append(ai_message)

    return {
        "messages": state["messages"]
    }

def tools_router(state: BasicChatBot):
    last_message = state["messages"][-1]

    if (hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else:
        return END


tool_node = ToolNode(tools=tools)

graph = StateGraph(BasicChatBot)

graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tool_node", "chatbot")

Maya = graph.compile(checkpointer=memory)

config = {"configurable": {
    "thread_id": "chat-thread-1"
}}

if __name__ == "__main__":
    while True:
        user_input = input("User: ")

        result = Maya.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)

        print("Maya:", result["messages"][-1].content)