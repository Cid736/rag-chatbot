# Bug Log — RAG Chatbot

## Acción manual requerida — 2026-06-25

### [CRITICAL] Groq API key expuesta en `.env`
- La clave `GROQ_API_KEY` está commiteada en `.env` (misma clave que cv-bot).
- **Acción:** Revocar y regenear en console.groq.com. Añadir `.env` al `.gitignore`.
