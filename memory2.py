from llm import llm
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

conversation = ConversationChain(llm=llm, memory=ConversationBufferWindowMemory(k=1))

result = conversation.invoke({
    "input": "我姐姐明天要过生日，我需要一束生日花束。"
})
result = conversation.invoke("她喜欢粉色玫瑰，颜色是粉色的。")

result = conversation("我又来了，还记得我昨天为什么要来买花吗？")
print(result)
