import sys
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Forzar impresión UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Cargar embeddings y vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vectorstore = FAISS.load_local("vectorstore_faiss", embedding_model, allow_dangerous_deserialization=True)

# LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key="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"
)

# Prompt
prompt = PromptTemplate.from_template(
    "Respondé en español de forma clara y concisa usando solo los documentos proporcionados.\n"
    "Si no hay información suficiente, respondé: 'No se encontró información relevante en la legislación disponible.'\n\n"
    "Contexto:\n{context}\n\nPregunta: {question}\nRespuesta:"
)

# Función principal
def buscar_y_responder(pregunta):
    docs_and_scores = vectorstore.similarity_search_with_score(pregunta, k=5)
    threshold = 0.65
    docs_filtrados = [doc for doc, score in docs_and_scores if score >= threshold]

    if not docs_filtrados:
        return {
            "result": "No se encontró información relevante en la legislación disponible.",
            "source_documents": []
        }

    # Combinar texto de contexto
    contexto = "\n\n".join([doc.page_content for doc in docs_filtrados])
    prompt_text = prompt.format(context=contexto, question=pregunta)

    # Llamar al modelo
    respuesta = llm.invoke(prompt_text)

    return {
        "result": respuesta.content.strip(),
        "source_documents": docs_filtrados
    }

# Interfaz
print("📘 Sistema de Consulta sobre Legislación Paraguaya")
print("Escribí tu pregunta o 'salir' para terminar.")
while True:
    pregunta = input("❓ Pregunta: >? ")
    if pregunta.lower() == "salir":
        print("👋 Hasta luego.")
        break

    if len(pregunta.split()) < 3:
        print("❌ Por favor, formulá una pregunta más clara.")
        continue

    resultado = buscar_y_responder(pregunta)
    respuesta = resultado["result"]
    fuentes = resultado.get("source_documents", [])

    print("✅ Respuesta:\n", respuesta)
    print("🔎 Fuente(s):")
    if fuentes:
        for doc in fuentes:
            meta = doc.metadata
            ley = meta.get("ley", "¿?")
            titulo = meta.get("titulo", "¿?")
            articulo = meta.get("articulo", "¿?")
            print(f" - Ley {ley} - {titulo} - Artículo {articulo}")
    else:
        print(" - No se encontraron fuentes relevantes.")
    print("—" * 60)
