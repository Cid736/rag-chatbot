# RAG Chatbot — LangChain + Groq + Embeddings locales

Chatbot de preguntas y respuestas sobre documentos propios usando un pipeline RAG (Retrieval-Augmented Generation). El modelo solo responde con informacion presente en los documentos cargados, evitando alucinaciones.

## Demo

```
RAG Chatbot  (Groq + embeddings locales)
─────────────────────────────────────────────
[v] 1 documento(s) cargado(s)
[v] 14 chunks generados
[v] Vector store listo

Listo. Escribe tu pregunta ('salir' para terminar).

Tu  -> ¿Cuanto tiempo tengo para reportar un incidente de seguridad?
Bot -> Segun la politica, cualquier incidente de seguridad debe reportarse
      en menos de 2 horas al equipo de ciberseguridad.
      [Fuente(s): politica_it.txt]
```

## Como funciona

```
Documentos .txt  ->  Chunks  ->  Embeddings locales  ->  ChromaDB (en memoria)
                                                              |
                              Pregunta del usuario  ->  Retrieval (Top-K chunks)
                                                              |
                                              LLM (Groq/Llama)  ->  Respuesta
```

1. **Carga** documentos `.txt` de la carpeta `docs/`
2. **Divide** el texto en chunks con solapamiento
3. **Genera embeddings** localmente con `sentence-transformers` (sin coste, sin API)
4. **Responde** recuperando los chunks mas relevantes y pasandolos al LLM como contexto

## Tecnologias

| Libreria | Uso |
|---|---|
| `LangChain` | Orquestacion del pipeline RAG |
| `Groq` | LLM en la nube (Llama 3.1, tier gratuito) |
| `sentence-transformers` | Embeddings locales (sin API) |
| `ChromaDB` | Vector store en memoria |

## Instalacion

```bash
# 1. Clonar el repositorio
git clone https://github.com/Cid736/rag-chatbot.git
cd rag-chatbot

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API key de Groq (gratis en https://console.groq.com)
cp .env.example .env
# Edita .env e inserta tu GROQ_API_KEY
```

## Uso

```bash
# Añade tus documentos .txt en la carpeta docs/
# ya incluye docs/politica_it.txt como ejemplo

python main.py
```

## Añadir tus propios documentos

Coloca archivos `.txt` en la carpeta `docs/` y ejecuta `python main.py`. El pipeline los carga automaticamente.

## Posibles extensiones

- [ ] Soporte PDF y DOCX
- [ ] Persistencia del vector store en disco
- [ ] Interfaz web con Streamlit
- [ ] Historial de conversacion
- [ ] Swap de Groq por modelo local con Ollama

## Historial de versiones

**v0.1.1** — 2026-06-24
- Fix: los errores del LLM ahora se capturan y reportan en lugar de terminar la sesión abruptamente
- Fix: reemplazados caracteres de marca y dibujo de caja que causaban crash de encoding en Windows (CP1252)

**v0.1.0** — 2026-05-01
- Publicación inicial: ingesta de documentos TXT, embeddings locales, LLM Groq, citas de fuentes
