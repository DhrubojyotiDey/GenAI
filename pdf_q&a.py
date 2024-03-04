import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import faiss
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key='AIzaSyC_aMEC-_z06kkO6XGO25mDKABS1jZCEfc')

def find_pdf_text(pdf_file):
    text=""
    for pdf in pdf_file:
        pdf_file=PdfReader(pdf)
        for page in pdf_file.pages:
            text+=page.extract_text()
    return text

def get_text_chunk(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap = 1000)
    chunks=text_splitter.split_text(text)
    return chunks

def get_vecor_store(text_chunks):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embeddings=001")
    vector_store=faiss.from_text(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_qa_chain():
    prompt_temp=""""Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:"""

    model=ChatGoogleGenerativeAI(model="gemini-pro", temperature=.1)
    Prompt=PromptTemplate(template=prompt_temp, input_variables=["content", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=Prompt)
    return chain