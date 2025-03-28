from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage
from llm import get_llm
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()

# history = ChatMessageHistory()
# history.add_message(HumanMessage(content="hi!"))
# history.add_message(AIMessage(content="whats up?"))
# messages = history.messages
# print(messages)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Answer all questions to the best of your ability.
    You are talkative and provides lots of specific details from its context. 
    If the you does not know the answer to a question, it truthfully says you do not know."""),
    MessagesPlaceholder("history_message"),
]);

chain = prompt | llm

history = ChatMessageHistory()
history.add_message(HumanMessage(content="hi, my name is Kai"))
res1 = chain.invoke({
    'history_message': history.messages
})
history.add_message(res1)
history.add_message(HumanMessage(content="What is my name?"))

res2 = chain.invoke({
    'history_message': history.messages
})
print(res2)