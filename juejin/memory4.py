from llm import get_llm
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from memory3 import summary_chain

llm = get_llm()
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are a helpful assistant. Answer all questions to the best of your ability.

        Here is the chat history summary:
        {history_summary}
     """),
    ("human", "{input}")
])
summary = ""
history = ChatMessageHistory()

def add_human_message(message):
    history.add_user_message(message)

def add_ai_message(message):
    history.add_ai_message(message)
    global summary
    new_summary = summary_chain.invoke({
        "summary": summary,
        "new_lines": "\n".join([f"{msg.type}: {msg.content}" for msg in history.messages])
    })
    history.clear()
    summary = new_summary

chat_chain = {
    "input": RunnablePassthrough(func=add_human_message)
} | RunnablePassthrough.assign(history_summary=lambda x: summary) | chat_prompt | llm | StrOutputParser() | RunnablePassthrough(func=add_ai_message)

response = chat_chain.invoke("我现在饿了")
# print(response)
response2 = chat_chain.invoke("我今天想吃方便面")
print(response2)
