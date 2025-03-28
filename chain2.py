from llm import llm
from langchain.prompts import PromptTemplate

template = """
    你是一个植物学家。给定花的名称和类型，你需要为这种花写一个200字左右的介绍。

    花名: {name}
    颜色: {color}
    植物学家: 这是关于上述花的介绍:
"""

prompt_template = PromptTemplate.from_template(template)

template2 = """
    你是一位鲜花评论家。给定一种花的介绍，你需要为这种花写一篇200字左右的评论。

    鲜花介绍:
    {introduction}
    花评人对上述花的评论:
"""

prompt_template2 = PromptTemplate.from_template(template2)

template3 = """
    你是一家花店的社交媒体经理。给定一种花的介绍和评论，你需要为这种花写一篇社交媒体的帖子，300字左右。

    鲜花介绍:
    {introduction}
    花评人对上述花的评论:
    {review}

    社交媒体帖子:
"""

prompt_template3 = PromptTemplate.from_template(template3)

chain = prompt_template | llm
result = chain.invoke({'name': '玫瑰', 'color': '红色'})
# print(result.content)

chain2 = prompt_template2 | llm
result2 = chain2.invoke({'introduction': result.content})
# print(result2.content)

chain3 = prompt_template3 | llm
result3 = chain3.invoke({'introduction': result.content,'review': result2.content})
print(result3.content)

