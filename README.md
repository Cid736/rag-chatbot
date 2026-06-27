<p align="center">
  <a href="#english">🇬🇧 English</a> &nbsp;·&nbsp; <a href="#español">🇪🇸 Español</a>
</p>

---

<a name="english"></a>

# RAG Chatbot — LangChain + Groq + Local Embeddings

Q&A chatbot over your own documents using a RAG (Retrieval-Augmented Generation) pipeline. The model only answers with information present in the loaded documents, avoiding hallucinations.

## Demo

```
RAG Chatbot  (Groq + local embeddings)
─────────────────────────────────────────────
[v] 1 document(s) loaded
[v] 14 chunks generated
[v] Vector store ready

Ready. Type your question ('exit' to quit).

You  -> How long do I have to report a security incident?
Bot  -> According to the policy, any security incident must be reported
        within 2 hours to the cybersecurity team.
        [Source(s): it_policy.txt]
```

## How it works

```
.txt documents  ->  Chunks  ->  Local embeddings  ->  ChromaDB (in memory)
                                                              |
                              User question  ->  Retrieval (Top-K chunks)
                                                              |
                                              LLM (Groq/Llama)  ->  Answer
```

1. **Load** `.txt` documents from the `docs/` folder
2. **Split** text into overlapping chunks
3. **Generate embeddings** locally with `sentence-transformers` (free, no API)
4. **Answer** by retrieving the most relevant chunks and passing them as context to the LLM

## Stack

| Library | Purpose |
|---|---|
| `LangChain` | RAG pipeline orchestration |
| `Groq` | Cloud LLM (Llama 3.1, free tier) |
| `sentence-transformers` | Local embeddings (no API) |
| `ChromaDB` | In-memory vector store |

## Setup

```bash
git clone https://github.com/Cid736/rag-chatbot.git
cd rag-chatbot
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GROQ_API_KEY (free at https://console.groq.com)
```

## Usage

```bash
# Add your .txt documents to the docs/ folder
python main.py
```

## Possible extensions

- [ ] PDF and DOCX support
- [ ] Persistent vector store on disk
- [ ] Web interface with Streamlit
- [ ] Conversation history
- [ ] Swap Groq for a local model with Ollama

## Changelog

**v0.1.1** — 2026-06-24
- Fix: LLM errors now caught and reported gracefully instead of crashing the session
- Fix: replace checkmark and box-drawing characters that caused encoding crash on Windows (CP1252)

**v0.1.0** — 2026-05-01
- Initial release: TXT document ingestion, local embeddings, Groq LLM, source citations

## Security

Automated security reviews are powered by [Claude](https://claude.ai) (Anthropic AI) and run on every significant change to detect vulnerabilities, insecure patterns and dependency risks. Findings are tracked in [`BUGLOG.md`](BUGLOG.md).

**Last review:** 2026-06-28 — 3 issues found (1 critical manual action required, 1 high, 1 low) — code fixes applied; see manual action below.

| Severity | File | Finding | Status |
|----------|------|---------|--------|
| CRITICAL ⚠️ | `.env` / git history | Groq API key committed to git history. **Rotate immediately at console.groq.com.** The key cannot be scrubbed by a code fix — you must revoke it. | Manual action required |
| HIGH | `main.py` | Prompt injection — user input was concatenated directly into the LLM prompt without structural separation. A crafted question could override the system instruction and make the LLM ignore document context. Fixed: context and question are now wrapped in XML-delimited tags (`<contexto>`, `<pregunta>`) with an explicit instruction to ignore embedded directives; max query length enforced (1000 chars). | Patched |
| LOW | `requirements.txt` | All dependencies were unpinned (no version constraints), allowing silent upgrades to breaking or vulnerable versions. `langchain-huggingface` was missing despite being imported. Fixed: all deps pinned to known-good versions. | Patched |

> **Action required:** Go to [console.groq.com](https://console.groq.com) → API Keys → revoke the exposed key and generate a new one. Update your local `.env`.

Found a vulnerability? Open an issue or contact directly.

---

<a name="español"></a>

# RAG Chatbot — LangChain + Groq + Embeddings Locales

Chatbot de preguntas y respuestas sobre tus propios documentos mediante un pipeline RAG (Retrieval-Augmented Generation). El modelo solo responde con información presente en los documentos cargados, evitando alucinaciones.

## Cómo funciona

1. **Carga** documentos `.txt` de la carpeta `docs/`
2. **Divide** el texto en fragmentos con solapamiento
3. **Genera embeddings** localmente con `sentence-transformers` (gratis, sin API)
4. **Responde** recuperando los fragmentos más relevantes y pasándolos como contexto al LLM

## Stack

| Librería | Función |
|---|---|
| `LangChain` | Orquestación del pipeline RAG |
| `Groq` | LLM en la nube (Llama 3.1, tier gratuito) |
| `sentence-transformers` | Embeddings locales (sin API) |
| `ChromaDB` | Base de datos vectorial en memoria |

## Instalación

```bash
git clone https://github.com/Cid736/rag-chatbot.git
cd rag-chatbot
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env
# Edita .env y añade tu GROQ_API_KEY (gratis en https://console.groq.com)
```

## Uso

```bash
# Añade tus documentos .txt a la carpeta docs/
python main.py
```

## Extensiones posibles

- [ ] Soporte de PDF y DOCX
- [ ] Base de datos vectorial persistente en disco
- [ ] Interfaz web con Streamlit
- [ ] Historial de conversación
- [ ] Sustituir Groq por un modelo local con Ollama

## Seguridad

Las revisiones de seguridad automatizadas utilizan [Claude](https://claude.ai) (Anthropic AI) y se ejecutan en cada cambio significativo para detectar vulnerabilidades, patrones inseguros y riesgos en dependencias. Los hallazgos se registran en [`BUGLOG.md`](BUGLOG.md).

**Última revisión:** 2026-06-28 — 3 vulnerabilidades encontradas (1 crítica acción manual requerida, 1 alta, 1 baja) — fixes de código aplicados; ver acción manual abajo.

| Severidad | Archivo | Hallazgo | Estado |
|-----------|---------|---------|--------|
| CRÍTICA ⚠️ | `.env` / historial git | API key de Groq commiteada en el historial de git. **Rotarla inmediatamente en console.groq.com.** No puede eliminarse con un fix de código — debes revocarla. | Acción manual requerida |
| ALTA | `main.py` | Prompt injection — la entrada del usuario se concatenaba directamente en el prompt del LLM sin separación estructural. Una pregunta manipulada podía anular la instrucción del sistema e ignorar el contexto de los documentos. Fix: contexto y pregunta ahora separados con delimitadores XML (`<contexto>`, `<pregunta>`) con instrucción explícita de ignorar directivas embebidas; longitud máxima de consulta aplicada (1000 chars). | Parcheado |
| BAJA | `requirements.txt` | Todas las dependencias sin versión fijada; `langchain-huggingface` faltante a pesar de importarse. Fix: todas las deps fijadas a versiones conocidas. | Parcheado |

> **Acción requerida:** Ve a [console.groq.com](https://console.groq.com) → API Keys → revoca la clave expuesta y genera una nueva. Actualiza tu `.env` local.

¿Encontraste una vulnerabilidad? Abre un issue o contacta directamente.
## Licencia

MIT
