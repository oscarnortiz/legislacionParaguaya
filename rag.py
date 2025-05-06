# -*- coding: utf-8 -*-

import os
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from dotenv import load_dotenv
load_dotenv()

# Cargar vectorstore
vectorstore = FAISS.load_local("vectorstore_faiss", HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Plantilla de prompt mejorada
plantilla = """
Eres un asistente jurídico entrenado en legislación paraguaya. Usá exclusivamente la información de los artículos legales proporcionados para responder.

Pregunta: {question}

Artículos relevantes:
{context}

Respuesta:
"""

prompt = PromptTemplate(
    template=plantilla,
    input_variables=["question", "context"]
)

llm_chain = LLMChain(llm=llm, prompt=prompt)
qa_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="context")

# Wrapper RetrievalQA
retrieval_chain = RetrievalQA(retriever=retriever, combine_documents_chain=qa_chain, return_source_documents=True)

def buscar_y_responder(pregunta):
    resultado = retrieval_chain.invoke({"query": pregunta})
    respuesta = resultado["result"]
    fuentes = resultado.get("source_documents", [])

    if not respuesta.strip():
        respuesta = "No se encontró información relevante en la legislación disponible."

    print("\n📝 Respuesta:\n", respuesta)
    print("\n🔎 Fuente(s):")
    for doc in fuentes:
        meta = doc.metadata
        print(f" - Ley {meta.get('nro_ley')} - {meta.get('titulo_ley')} - Artículo {meta.get('nro_articulo')}")


print("📚 Sistema de Consulta sobre Legislación Paraguaya")
print("Escribí tu pregunta o 'salir' para terminar.")

while True:
    pregunta = input("➤ Pregunta: >? ").strip()
    if pregunta.lower() in ["salir", "exit"]:
        break
    buscar_y_responder(pregunta)
