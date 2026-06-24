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
# 1. Clone the repository
git clone https://github.com/Cid736/rag-chatbot.git
cd rag-chatbot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Groq API key (free at https://console.groq.com)
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

## Usage

```bash
# Add your .txt documents to the docs/ folder
# docs/it_policy.txt is included as an example

python main.py
```

## Adding your own documents

Drop `.txt` files into the `docs/` folder and run `python main.py`. The pipeline loads them automatically.

## Possible extensions

- [ ] PDF and DOCX support
- [ ] Persistent vector store on disk
- [ ] Web interface with Streamlit
- [ ] Conversation history
- [ ] Swap Groq for a local model with Ollama

## Changelog

**v0.1.1** — 2026-06-24
- Fix: replace checkmark and box-drawing characters that caused encoding crash on Windows (CP1252)

**v0.1.0** — 2026-05-01
- Initial release: TXT document ingestion, local embeddings, Groq LLM, source citations
