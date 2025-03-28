from llm import get_llm
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder("history_message"),
    ("human", "{input}")
])

history = ChatMessageHistory()

chain = prompt | get_llm()

chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=lambda x: history,
    history_messages_key="history_message",
    input_messages_key="input"
)

res1 = chain_with_history.invoke({
    'input': 'hi, my name is Kai'
}, config={'configurable': {
    'session_id': '123456'
}})
# print(res1)
res2 = chain_with_history.invoke({
    'input': 'What is my name?'
}, config={
    'configurable': {
        'session_id': '123456'
    }
})
# print(res2)
print(history.messages)