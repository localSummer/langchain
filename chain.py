from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from llm import llm

# prompt = prompt_template.format(flower="玫瑰")

# print(prompt)

# 为 flower 和 season 定义响应模式字典
response_schemas = [
    ResponseSchema(name="flower", description="鲜花的名称"),
    ResponseSchema(name="season", description="鲜花的季节"),
    ResponseSchema(name="meaning", description="鲜花的花语")
]

# 将响应模式字典转换为结构化输出解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

template = "{flower}在{season}的花语是? 输出结构：{format_instructions}"
prompt_template = PromptTemplate(
    template=template,
    input_variables=["flower", "season"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)


input_list = [
    {"flower": "玫瑰",'season': "夏季"},
    {"flower": "百合",'season': "春季"},
    {"flower": "郁金香",'season': "秋季"}
]

# print(prompt_template.format(flower="玫瑰", season="夏季"))

llm_chain = prompt_template | llm

# result = llm_chain.invoke(input_list[0])
# 处理 input_list 中的每个输入
results = llm_chain.batch(input_list)

print(results[2].content)
