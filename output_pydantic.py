# 自定义输出解析器代码结构
class OutputParser:
    def __inti__(self):
        pass
    
    def get_format_instructions(self):
        # 返回一个字符串，指导如何格式化模型的输出
        pass
    
    def parser(self, model_output):
        # 解析模型的输出，转换为某种数据结构或格式
        pass
    
    def parse_with_prompt(self, model_output, prompt):
        # 基于原始提示解析模型的输出，转换为某种数据结构或格式
        pass
    
import os
from dotenv import load_dotenv
from langchain import output_parsers
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model=os.environ.get('OPEN_API_MODEL'),
    api_key=os.environ.get('OPEN_API_KEY'),
    base_url=os.environ.get('OPEN_API_BASE')
)

import pandas as pd

# 创建一个空的DataFrame，用于存储数据
df = pd.DataFrame(
    columns=['flower_type', 'price', 'description', 'reason'],
)

flowers = ["瑰", "百合", "康乃馨"]
prices = ["50", "30", "20"]

from pydantic import BaseModel, Field

# 定义一个Pydantic模型，用于解析模型的输出
class FlowerDescription(BaseModel):
    flower_type: str = Field(description="鲜花的种类")
    price: int = Field(description="鲜花的价格")
    description: str = Field(description="鲜花的描述文案")
    reason: str = Field(description="为什么要写这个文案")
    
from langchain.output_parsers import PydanticOutputParser

output_parsers = PydanticOutputParser(pydantic_object=FlowerDescription)

format_instructions = output_parsers.get_format_instructions()

# print(format_instructions)

from langchain.prompts import PromptTemplate

prompt_template = """
    您是一位专业的鲜花店文案撰写员。
    对于售价为 {price} 元的 {flower} ，您能提供一个吸引人的简短中文描述吗？{format_instructions}
"""

# 创建一个PromptTemplate实例
prompt = PromptTemplate.from_template(prompt_template, partial_variables={"format_instructions": format_instructions})

# print(prompt.format(price=prices[0], flower=flowers[0]))

for flower, price in zip(flowers, prices):
    # 构建一个Chain，将PromptTemplate和LLM和输出解析器连接起来
    chain = prompt | llm | output_parsers
    
    parsed_output = chain.invoke({"price": price, "flower": flower})
    
    # print(parsed_output.model_dump_json())
    
    # 将解析后的输出转换为JSON格式
    json_output = parsed_output.model_dump_json()
    
    # 将JSON格式的数据添加到DataFrame中
    df.loc[len(df)] = json_output

print(f"输出的数据是：{df.to_dict(orient='records')}")