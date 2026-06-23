"""
RAG Chatbot – LangChain + Groq (gratis) + Embeddings locales
"""

import os
import sys
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# ── Configuración ────────────────────────────────────────────────────────────

DOCS_DIR      = "./docs"
MODEL         = "llama-3.1-8b-instant"
EMBED_MODEL   = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50
TOP_K         = 3

PROMPT_TEMPLATE = """Usa únicamente el siguiente contexto para responder la pregunta.
Si la respuesta no está en los documentos, responde exactamente:
"No tengo información suficiente en los documentos cargados."

Contexto:
{context}

Pregunta: {question}
Respuesta:"""


# ── Pipeline RAG ─────────────────────────────────────────────────────────────

def load_documents(directory: str):
    loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader,
                             loader_kwargs={"encoding": "utf-8"})
    docs = loader.load()
    if not docs:
        print(f"[!] No se encontraron documentos en '{directory}'.")
        sys.exit(1)
    print(f"[✓] {len(docs)} documento(s) cargado(s)")
    return docs


def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)
    print(f"[✓] {len(chunks)} chunks generados")

    print("[~] Cargando modelo de embeddings (primera vez puede tardar)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    print("[✓] Vector store listo")
    return vectorstore


def build_chain(vectorstore):
    llm = ChatGroq(model=MODEL, temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE,
    )

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    if not os.getenv("GROQ_API_KEY"):
        print("[!] Falta la variable de entorno GROQ_API_KEY.")
        print("    Obtén tu key gratis en: https://console.groq.com")
        print("    Crea un archivo .env con: GROQ_API_KEY=gsk_...")
        sys.exit(1)

    print("\n🤖  RAG Chatbot  (Groq + embeddings locales)")
    print("─" * 45)

    docs             = load_documents(DOCS_DIR)
    vectorstore      = build_vectorstore(docs)
    chain, retriever = build_chain(vectorstore)

    print("\nListo. Escribe tu pregunta ('salir' para terminar).\n")

    while True:
        try:
            query = input("Tú → ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[!] Sesión terminada.")
            break

        if not query:
            continue
        if query.lower() in ("salir", "exit", "quit", "q"):
            break

        answer  = chain.invoke(query)
        sources = sorted({
            os.path.basename(doc.metadata.get("source", "desconocido"))
            for doc in retriever.invoke(query)
        })

        print(f"\nBot → {answer}")
        print(f"      [Fuente(s): {', '.join(sources)}]\n")


if __name__ == "__main__":
    main()
