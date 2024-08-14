import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.prompts.prompts import RAG_SEARCH_PROMPT_TEMPLATE
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

vectorstore = Chroma(persist_directory="db", embedding_function=embeddings)

# Semantic vector search
vectorstore_retreiver = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template(RAG_SEARCH_PROMPT_TEMPLATE)

llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

# build retrieval chain using LCEL
# this will take the user query and generate the answer
rag_chain = (
    {"context": vectorstore_retreiver, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
