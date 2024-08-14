import os
from pydantic import Field
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.prompts.prompts import RAG_SEARCH_PROMPT_TEMPLATE
from ..base_tool import BaseTool

class KnowledgeSearchTool(BaseTool):
    """
    A tool that searches a knowledge base and answers user queries based on the stored information.
    """

    query: str = Field(description="User's query to search in the knowledge base")

    def __init__(self):
        super().__init__()
        self.retriever = self.load_retriever()

    def load_retriever(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vectorstore = Chroma(persist_directory="db", embedding_function=embeddings)
        vectorstore_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        prompt = ChatPromptTemplate.from_template(RAG_SEARCH_PROMPT_TEMPLATE)

        llm = ChatGroq(model="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY"))
        app = (
            {"context": vectorstore_retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return app

    def search_knowledge_base(self, query: str) -> str:
        response = self.retriever.invoke(query)
        return str(response)

    def run(self):
        return self.search_knowledge_base(self.query)