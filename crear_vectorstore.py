# -*- coding: utf-8 -*-

import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Leer archivos CSV desde la carpeta local 'data'
articulos = pd.read_csv("data/articulos.csv")
leyes = pd.read_csv("data/leyes.csv")

# Unir título de ley a cada artículo
articulos = articulos.merge(leyes, on="ley", how="left")

# Preparar documentos para FAISS, incluyendo el título de la ley en el contenido
docs = []
for _, row in articulos.iterrows():
    metadata = {
        "nro_ley": row["ley"],
        "titulo_ley": row["titulo"],
        "nro_articulo": row["articulo"]
    }
    contenido = f"Ley {row['ley']} - {row['titulo']} - Artículo {row['articulo']}\n{row['texto']}"
    docs.append(Document(page_content=contenido, metadata=metadata))

# Crear embeddings y vectorstore
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("vectorstore_faiss")

print("✅ Vectorstore generado y guardado exitosamente.")
