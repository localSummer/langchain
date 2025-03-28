from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains.llm import LLMChain
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from llm import get_llm, llm_embedding
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import os
import streamlit

class ChatbotWithMemory:
    def __init__(self):
        self.chat = get_llm()
        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template("你是一个花卉行家。你通常的回答不超过30字。"),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation = LLMChain(
            llm=self.chat,
            prompt=self.prompt,
            memory=self.memory,
            verbose=True
        )
    
    def chat_loop(self):
        print("Chatbot 已启动! 输入'exit'来退出程序。")
        while True:
            user_input = input("你: ")
            # 如果用户输入“exit”，则退出循环
            if user_input.lower() == 'exit':
                print("再见!")
                break
            response = self.conversation.invoke({"question": user_input})
            print(f"Chatbot: {response}")

class ChatboxWithRetrieval:
    def __init__(self, dir):
        base_dir = dir
        documents = []
        for file in os.listdir(base_dir):
            file_path = os.path.join(base_dir, file)
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith(".docx") or file.endswith(".doc"):
                loader = Docx2txtLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith(".txt"):
                loader = TextLoader(file_path)
                documents.extend(loader.load())
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        all_splits = text_splitter.split_documents(documents)
        
        self.llm = get_llm()
        self.llm_embedding = llm_embedding
        self.vector_store = Chroma.from_documents(documents=all_splits, embedding=self.llm_embedding, persist_directory="chatbot_db")
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
        )
        
        retriever = self.vector_store.as_retriever()
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            verbose=True
        )
    
    def chat_loop(self):
        print("Chatbot 已启动! 输入'exit'来退出程序。")
        while True:
            user_input = input("你: ")
            # 如果用户输入“exit”，则退出循环
            if user_input.lower() == 'exit':
                print("再见!")
                break
            response = self.qa.invoke({"question": user_input})  
            print(f"Chatbot: {response}")
            
def main():
    streamlit.title("易速鲜花聊天客服")
    if "bot" not in streamlit.session_state:
        streamlit.session_state.bot = ChatboxWithRetrieval("docs")
    user_input = streamlit.text_input("请输入你的问题：")
    if user_input:
        response = streamlit.session_state.bot.qa.invoke({"question": user_input})
        streamlit.write(f"Chatbot: {response['answer']}")

if __name__ == "__main__":
    main()