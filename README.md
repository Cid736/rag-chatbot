# RAG Chatbot — LangChain + Groq + Embeddings locales

Chatbot de preguntas y respuestas sobre documentos propios usando un pipeline **RAG** (Retrieval-Augmented Generation). El modelo solo responde con información presente en los documentos cargados, evitando alucinaciones.

## Demo

```
🤖  RAG Chatbot  (Groq + embeddings locales)
─────────────────────────────────────────────
[✓] 1 documento(s) cargado(s)
[✓] 14 chunks generados
[✓] Vector store listo

Listo. Escribe tu pregunta ('salir' para terminar).

Tú → ¿Cuánto tiempo tengo para reportar un incidente de seguridad?
Bot → Según la política, cualquier incidente de seguridad debe reportarse
      en menos de 2 horas al equipo de ciberseguridad.
      [Fuente(s): politica_it.txt]
```

## Cómo funciona

```
Documentos .txt  →  Chunks  →  Embeddings locales  →  ChromaDB (en memoria)
                                                              ↓
                              Pregunta del usuario → Retrieval (Top-K chunks)
                                                              ↓
                                              LLM (Groq/Llama) → Respuesta
```

1. **Carga** documentos `.txt` de la carpeta `docs/`
2. **Divide** el texto en chunks con solapamiento
3. **Genera embeddings** localmente con `sentence-transformers` (sin coste, sin API)
4. **Responde** recuperando los chunks más relevantes y pasándolos al LLM como contexto

## Tecnologías

| Librería | Uso |
|---|---|
| `LangChain` | Orquestación del pipeline RAG |
| `Groq` | LLM en la nube (Llama 3.1, tier gratuito) |
| `sentence-transformers` | Embeddings locales (sin API) |
| `ChromaDB` | Vector store en memoria |

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/rag-chatbot.git
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

Coloca archivos `.txt` en la carpeta `docs/` y ejecuta `python main.py`. El pipeline los carga automáticamente.

## Posibles extensiones

- [ ] Soporte PDF y DOCX
- [ ] Persistencia del vector store en disco
- [ ] Interfaz web con Streamlit
- [ ] Historial de conversación
- [ ] Swap de Groq por modelo local con Ollama
