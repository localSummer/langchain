from langchain_core.documents import Document
from llm import get_llm, llm_embedding
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableSequence
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()

persist_directory = "db/rag_db"

def get_split_docs():
    text_loader = TextLoader('data/qiu.txt', encoding='utf-8')
    # 加载文档
    docs = text_loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    split_docs = splitter.split_documents(docs)
    return split_docs

def load_to_vector_db():
    split_docs = get_split_docs()
    Chroma.from_documents(split_docs, llm_embedding, persist_directory=persist_directory)

def get_vector_retriever():
    db = Chroma(persist_directory=persist_directory, embedding_function=llm_embedding)
    retriever = db.as_retriever(search_kwargs={'k': 2})
    return retriever

def conver_docs_to_string(docs: list[Document]) -> str:
    return '\n'.join([doc.page_content for doc in docs])

# load_to_vector_db()

retriever = get_vector_retriever()

# response = retriever.invoke("原文中，谁提出了宏原子的假设？并详细介绍给我宏原子假设的理论")

context_retriever_chain = RunnableSequence(
    lambda x: x['question'],
    retriever,
    conver_docs_to_string,
)

# response = context_retriever_chain.invoke({
#     'question': '原文中，谁提出了宏原子的假设？并详细介绍给我宏原子假设的理论'
# })
# print(response)

template = """
你是一个熟读刘慈欣的《球状闪电》的终极原著党，精通根据作品原文详细解释和回答问题，你在回答时会引用作品原文。
并且回答时仅根据原文，尽可能回答用户问题，如果原文中没有相关内容，你可以回答“原文中没有相关内容”，

以下是原文中跟用户回答相关的内容：
{context}

现在，你需要基于原文，回答以下问题：
{question}
"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = {
    'context': context_retriever_chain,
    'question': lambda input: input['question']
} | prompt | llm | StrOutputParser()

# answer = rag_chain.invoke({
#     'question': "什么是球状闪电"
# })

# print(answer)

answer = rag_chain.invoke({
    'question': "详细描述原文中有什么跟直升机相关的场景"
})

print(answer)
