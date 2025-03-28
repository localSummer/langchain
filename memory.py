from llm import llm
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

chain = ConversationChain(llm=llm, memory=ConversationBufferMemory())

chain.invoke({
    'input': '你好'
})

print(chain.memory.buffer)
