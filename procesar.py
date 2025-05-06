import pandas as pd
import re

# Cargamos el archivo
df = pd.read_csv("data/articulos.csv", encoding="utf-8")


# Limpiamos espacios en blanco innecesarios
df['articulo'] = df['articulo'].astype(str).str.strip()
df['texto'] = df['texto'].astype(str).str.strip()

# Unificamos el formato de encabezado de artículo (Art., ARTÍCULO, etc.)
def normalize_article_header(text):
    text = text.strip()
    # Reemplazar variantes como "Art. 1°.-", "art.1.-", etc.
    text = re.sub(r'(?i)\bArt[íi]?[cC]?[uU]?[lL]?[oO]?[ ]*\.*[ ]*(\d+)[°º]?[\.-]*', r'ARTÍCULO \1.-', text)
    return text

df['articulo'] = df['articulo'].apply(normalize_article_header)

# Normalizamos comillas, espacios, caracteres especiales
df['texto'] = df['texto'].str.replace(r'\s+', ' ', regex=True)
df['texto'] = df['texto'].str.replace(r'\xa0', ' ', regex=True)
df['texto'] = df['texto'].str.replace(r'\u200b', '', regex=True)

# Revisamos artículos vacíos
df = df[df['articulo'].str.len() > 5]

# Exportamos archivo limpio
clean_path = "data/articulos_limpio.csv"
df.to_csv(clean_path, index=False)

print(df.head(20))  # Muestra los primeros 20 artículos normalizados

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os

# Cargamos el archivo CSV con los artículos
csv_path = "data/articulos.csv"
df = pd.read_csv(csv_path)

# Llenamos valores nulos para evitar errores al generar embeddings
df['texto'] = df['texto'].fillna("")

# Usamos un modelo multilingüe para obtener embeddings
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

# Generamos los embeddings para cada artículo
embeddings = model.encode(df['texto'].tolist(), show_progress_bar=True)

# Convertimos los embeddings a un DataFrame y los unimos al original
embeddings_df = pd.DataFrame(embeddings, columns=[f"dim_{i}" for i in range(embeddings.shape[1])])
df_embeddings = pd.concat([df.reset_index(drop=True), embeddings_df], axis=1)

# Guardamos el resultado
output_path = "data/articulos_con_embeddings.csv"
df_embeddings.to_csv(output_path, index=False)

print(df.head(20))  # Muestra los primeros 20 artículos normalizados


