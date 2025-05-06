import os

def extraer_articulos():
    import extraerArticulos
    print("✅ Artículos extraídos")

def procesar_articulos():
    import procesar
    print("✅ Artículos procesados")

def crear_vectorstore():
    import crear_vectorstore
    print("✅ Vectorstore creado")

def iniciar_chat_rag():
    import rag

if __name__ == "__main__":
    print("=== Sistema de Legislación Paraguaya ===")
    print("1. Extraer artículos desde BACN")
    print("2. Procesar artículos y guardar CSV")
    print("3. Crear vectorstore (indexar)")
    print("4. Iniciar sistema de preguntas y respuestas")
    print("0. Salir")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        extraer_articulos()
    elif opcion == "2":
        procesar_articulos()
    elif opcion == "3":
        crear_vectorstore()
    elif opcion == "4":
        iniciar_chat_rag()
    elif opcion == "0":
        print("👋 Programa finalizado.")
    else:
        print("❌ Opción inválida.")
