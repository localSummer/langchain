import os
from dotenv import load_dotenv
from langchain.prompts import AIMessagePromptTemplate, ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, FewShotPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

samples = [
    {
        "question": "鲜花价格是多少？",
        "answer": "我们鲜花价格因品种和季节有所不同，一般一束普通鲜花价格在50到200元之间。"
    },
    {
        "question": "我想送花给朋友，有什么推荐吗？",
        "answer": "如果您朋友喜欢淡雅的花，推荐百合花；要是喜欢鲜艳色彩，玫瑰是个不错的选择。"
    },
    {
        "question": "鲜花怎么保养？",
        "answer": "鲜花需要保持充足的水分，避免阳光直射，定期更换水并修剪茎部。"
    },
    {
        "question": "有没有适合送给母亲的花？",
        "answer": "康乃馨是很适合送给母亲的花，它象征着母爱，有多种颜色可供选择。"
    },
    {
        "question": "鲜花可以保存多久？",
        "answer": "一般鲜花在正常保养下可以保存3到7天，具体时间取决于鲜花品种和环境。"
    }
]

messages = []

system_template = SystemMessagePromptTemplate.from_template(
    "你是鲜花店客服，根据以下示例回答客户问题"
)

messages.append(system_template)

human_template = "用户的问题是：{question}"

for example in samples:
    messages.append(HumanMessagePromptTemplate.from_template(f"问题是：{example['question']}，答案是："))
    messages.append(AIMessagePromptTemplate.from_template(example["answer"]))

messages.append(HumanMessagePromptTemplate.from_template(human_template))

prompt = ChatPromptTemplate.from_messages(messages)

print(prompt.format(question="鲜花价格是多少？"))

chat_modal = ChatOpenAI(model=os.environ.get('OPEN_API_MODEL'), openai_api_key=os.environ.get('OPEN_API_KEY'), openai_api_base=os.environ.get('OPEN_API_BASE'))

chain = prompt | chat_modal

result = chain.invoke({"question": "鲜花价格是多少？"})

print(result.content)
