from llm import get_llm
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.callbacks.manager import get_openai_callback

llm = get_llm(temperature=0.5)

conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())

with get_openai_callback() as cb:
    # 第一天的对话
    # 回合1
    conversation.invoke("我姐姐明天要过生日，我需要一束生日花束。")
    print("第一次对话后的记忆:", conversation.memory.buffer)

    # 回合2
    conversation.invoke("她喜欢粉色玫瑰，颜色是粉色的。")
    print("第二次对话后的记忆:", conversation.memory.buffer)

    # 回合3 （第二天的对话）
    conversation.invoke("我又来了，还记得我昨天为什么要来买花吗？")
    print("/n第三次对话后时提示:/n",conversation.prompt.template)
    print("/n第三次对话后的记忆:/n", conversation.memory.buffer)
    
print("\n总计使用的tokens:", cb.total_tokens)