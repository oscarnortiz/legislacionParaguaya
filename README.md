# Sistema de Consulta sobre Legislación Paraguaya

Este proyecto permite realizar preguntas en lenguaje natural sobre leyes paraguayas, utilizando técnicas de Recuperación Aumentada por Generación (RAG). Integra extracción de artículos desde la BACN, procesamiento de textos, vectorización y un sistema conversacional con un LLM.

## Estructura del Proyecto

- `extraerArticulos.py`: Extrae artículos de leyes desde el portal de la BACN Paraguay y guarda los datos en `articulos.csv`.
- `procesar.py`: Limpia y normaliza los artículos extraídos, vinculándolos con su ley y título (`leyes.csv`).
- `crear_vectorstore.py`: Crea un vectorstore FAISS a partir de los artículos procesados, utilizando embeddings de HuggingFace.
- `rag.py`: Inicia el sistema de preguntas y respuestas, cargando el vectorstore y respondiendo con base en los artículos legales.
- `main.py`: Menú interactivo que permite ejecutar cada etapa del flujo de forma ordenada.

## Requisitos

- Python 3.10+
- Paquetes:
  - `langchain`
  - `langchain-openai`
  - `langchain-community`
  - `openai`
  - `faiss-cpu`
  - `pandas`
  - `beautifulsoup4`
  - `requests`
  - `python-dotenv`
  
## 📚 Corpus legal utilizado

Fuentes oficiales extraídas de la Biblioteca y Archivo del Congreso Nacional (BACN):

- Constitución Nacional
- Código Laboral (Ley N° 213/93)
- Código Civil (Ley N° 1183/85)
- Código Penal (Ley N° 1160/97)
- Código Electoral Paraguayo
- Ley de Tránsito (Ley N° 5016/14)
- Ley de Telecomunicaciones (Ley N° 642/95)
- Ley de la Niñez y Adolescencia (Ley N° 1680/01)
- Ley de Protección Integral a las Mujeres (Ley N° 5777/16)
- Ley de Migraciones (Ley N° 6984/22)
- Y otras normativas clave...


## 🛠️ Instalación

1. Para clonar y poner a punto este repositorio:
   ```bash
   git clone https://github.com/oscarnortiz/legislacionParaguaya.git
   cd legislacionParaguaya
   python3 -m venv venv
   pip install -r requirements.txt
   ```

## Nota

Se requiere una clave API de OpenAI. Guardarla en un archivo .env como:
```bash
OPENAI_API_KEY=sk-xxxxx
```

## Uso

Desde terminal, ejecutar:
```bash
python main.py
```

Y elegir entre:

1. Extraer artículos desde la web de BACN
2. Procesar artículos y generar los CSV
3. Crear el vectorstore
4. Iniciar el sistema de preguntas y respuestas

## Ejemplo de Uso

📚 Sistema de Consulta sobre Legislación Paraguaya
Escribí tu pregunta o 'salir' para terminar.
➤ Pregunta: ¿Cuáles son los requisitos para adoptar en Paraguay?

📝 Respuesta:
Para adoptar un menor en Paraguay, se deben cumplir...