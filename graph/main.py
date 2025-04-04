from langgraph.graph import StateGraph, MessagesState
from llm import llm

graph_builder = StateGraph(MessagesState)

# 定义 chatbot 节点
def chatbot(state: MessagesState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

# 构建和编译图
from langgraph.graph import START, END

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# 运行图
from langchain_core.messages import HumanMessage

response = graph.invoke({"messages": [HumanMessage(content="北京今天天气怎么样?")]})

response["messages"][-1].pretty_print()
