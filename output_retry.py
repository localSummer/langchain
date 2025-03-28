# 定义一个模板字符串，这个模板将用于生成提问
template = """Based on the user question, provide an Action and Action Input for what step should be taken.
    {format_instructions}
    Question: {query}
    Response:
"""

from pydantic import BaseModel, Field

class Action(BaseModel):
    action: str = Field(description="action to take")
    action_input: str = Field(description="input to the action")
    
from langchain.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=Action)

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

prompt_value = prompt.format_prompt(query="What are the colors of Orchid?")

bad_response = '{"action": "search"}'

from langchain.output_parsers import OutputFixingParser
from llm import llm


# fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

# parser_result = fix_parser.parse(bad_response)

# print(parser_result)

from langchain.output_parsers import RetryWithErrorOutputParser

retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=llm)

parset_result = retry_parser.parse_with_prompt(bad_response, prompt_value)

print(parset_result.model_dump_json())