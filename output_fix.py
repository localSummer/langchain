from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model=os.environ.get('OPEN_API_MODEL'),
    api_key=os.environ.get('OPEN_API_KEY'),
    base_url=os.environ.get('OPEN_API_BASE'),
)

class Flower(BaseModel):
    name: str = Field(description="鲜花的名称")
    colors: List[str] = Field(description="鲜花的颜色")
    
flower_query = "Generate the charaters for a random flower"

misformatted = "{'name': '康乃馨', 'colors': ['粉红色','白色','红色','紫色','黄色']}"

parser = PydanticOutputParser(pydantic_object=Flower)
new_parser = OutputFixingParser.from_llm(llm=llm, parser=parser)

# 在 OutputFixingParser 内部，调用了原有的 PydanticOutputParser，如果成功，就返回；如果失败，它会将格式错误的输出以及格式化的指令传递给大模型，并要求LLM 进行相关的修复。
result = new_parser.parse(misformatted)

print(result)