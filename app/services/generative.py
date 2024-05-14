from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.assistant import AssistantSchema

def set_embedding(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
    chunks = text_splitter.split_documents(data)
    Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(), 
        persist_directory="db"
    )

def get_knowledge_by_url(url: List[str]):
    loader = UnstructuredURLLoader(url)
    pages = loader.load()
    return pages

def get_embeddings(question):
    db = Chroma(persist_directory="db", embedding_function=OpenAIEmbeddings())
    return db.similarity_search(query=question, k=3)

def get_assistant(name: str, db: Session):
    assistant = db.query(AssistantSchema).filter(AssistantSchema.name == name).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant

def get_prompt(assistant: AssistantSchema):
    template = """
        {description}
        CONTEXTO: {context}
        QUESTION: {question}
        Exemplo de como se comportar: {examples}
        Seja breve e responda a pergunta com base no CONTEXTO fornecido.
    """
    template = template.replace("{description}", assistant.description)
    template = template.replace("{examples}", assistant.interaction_example)
    return template

def get_generative_answer(template_question: str, learning_retriever: str, question: str):
    QA_CHAIN_PROMPT = PromptTemplate(template=template_question, input_variables=["description","context", "question", "examples"])
    llm = ChatOpenAI(model="gpt-3.5-turbo",temperature=1)
    chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)
    answer = chain({
        "input_documents": learning_retriever, 
        "question": question 
    }, return_only_outputs=True)
    return answer
