from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from llm import get_llm
from tools.parse_tool import letter_parser

def generate_letter(information):
    letter_template = """
        下面是这个人的微博信息 {information}
         请你帮我:
         1. 写一个简单的总结
         2. 挑两件有趣的事情说一说
         3. 找一些他比较感兴趣的事情
         4. 写一篇热情洋溢的介绍信
         {format_instructions}
    """
    
    prompt_template = PromptTemplate(
        template=letter_template,
        input_variables=["information"],
        partial_variables={
            "format_instructions": letter_parser.get_format_instructions()
        }
    )
    
    llm = get_llm()
    
    chain = prompt_template | llm | letter_parser
    result = chain.invoke({"information": information})
    return result.model_dump_json()
    
    