from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

template = '你是一位专业顾问，负责为专注于{product}的公司起名'
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = '公司主打产品是{product_detail}。'
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chat = ChatOpenAI(model=os.environ.get('OPEN_API_MODEL'), openai_api_key=os.environ.get('OPEN_API_KEY'), openai_api_base=os.environ.get('OPEN_API_BASE'))

chain = prompt | chat

result = chain.invoke({'product': '鲜花装饰', 'product_detail': '创新的鲜花设计'})

print(result)



