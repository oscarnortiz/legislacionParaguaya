import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset con embeddings
df = pd.read_csv("data/articulos_con_embeddings.csv")

# Cargar el modelo
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

# Función para buscar los artículos más relevantes
def buscar_pregunta(pregunta, top_k=5):
    emb_pregunta = model.encode([pregunta])
    emb_articulos = df[[f"dim_{i}" for i in range(emb_pregunta.shape[1])]].values
    similitudes = cosine_similarity(emb_pregunta, emb_articulos)[0]
    df['similitud'] = similitudes
    resultados = df.sort_values(by="similitud", ascending=False).head(top_k)
    return resultados[['ley', 'articulo', 'texto', 'similitud']]

# Ejemplo de uso
query = input("Introduce tu pregunta legal: ")
resultados = buscar_pregunta(query)

# Mostrar resultados
print("\n🔎 Resultados más relevantes:\n")
for _, fila in resultados.iterrows():
    print(f"{fila['articulo']} (Ley {fila['ley']})\n{fila['texto']}\n---\n")
