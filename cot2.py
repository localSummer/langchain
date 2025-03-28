import os
from re import template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model=os.environ.get("OPEN_API_MODEL"),
    api_key=os.environ.get("OPEN_API_KEY"),
    base_url=os.environ.get("OPEN_API_BASE"),
)

system_template = "你是一个为花店电商公司工作的AI助手, 你的目标是帮助客户根据他们的喜好做出明智的决定"

system_cot_template = """
    作为一个为花店电商公司工作的AI助手，我的目标是帮助客户根据他们的喜好做出明智的决定。

    我会按部就班的思考，先理解客户的需求，然后考虑各种鲜花的涵义，最后根据这个需求，给出我的推荐。
    同时，我也会向客户解释我这样推荐的原因。
"""

system_prompt = SystemMessagePromptTemplate.from_template(system_template)
system_cot_prompt = SystemMessagePromptTemplate.from_template(system_cot_template)

human_propt = HumanMessagePromptTemplate.from_template("{human_input}")

chat_prompt = ChatPromptTemplate(messages=[system_prompt, system_cot_prompt, human_propt])

# print(chat_prompt.format(human_input="我想为我的女朋友购买一些花。她喜欢粉色和紫色。你有什么建议吗?"))

chain = chat_prompt | llm

result = chain.invoke({"human_input": "我想为我的女朋友购买一些花。她喜欢粉色和紫色。你有什么建议吗?"})

print(result.content)