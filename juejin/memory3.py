from llm import get_llm
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()

summary_prompt = ChatPromptTemplate.from_template(
    """
    Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary

    Current summary:
    {summary}

    New lines of conversation:
    {new_lines}

    New summary:
    """
)

summary_chain = summary_prompt | llm | StrOutputParser()
new_summary = summary_chain.invoke({"summary": "", "new_lines": "I'm 18"})
# print(new_summary)
new_summary2 = summary_chain.invoke({"summary": new_summary, "new_lines": "I'm male"})
print(new_summary2)