# Bug Log — RAG Chatbot

## Acción manual requerida — 2026-06-25

### [CRITICAL] Groq API key expuesta en `.env`
- La clave `GROQ_API_KEY` está commiteada en `.env` (misma clave que cv-bot).
- **Acción:** Revocar y regenear en console.groq.com. Añadir `.env` al `.gitignore`.

---

## 2026-06-28 — Revisión 2

### [HIGH] Prompt Injection
- **Archivo:** `main.py` líneas 28–36 (PROMPT_TEMPLATE)
- **Descripción:** La entrada del usuario se concatenaba directamente en el prompt del LLM mediante f-string sin ninguna separación estructural. Un usuario podía escribir "Ignora las instrucciones anteriores y..." para hacer que el LLM ignorara el contexto de los documentos y respondiera libremente.
- **Fix:** El template ahora usa delimitadores XML (`<contexto>`, `<pregunta>`) con una instrucción explícita de no seguir directivas contenidas en el contexto o la pregunta. Añadido límite máximo de 1000 caracteres por consulta (`MAX_QUERY_LEN`).

### [LOW] Dependencias sin versión fijada + `langchain-huggingface` faltante
- **Archivo:** `requirements.txt`
- **Descripción:** Todas las dependencias carecían de versión, permitiendo instalaciones silenciosas de versiones vulnerables o incompatibles. `langchain-huggingface` se importaba en el código pero no estaba declarada.
- **Fix:** Todas las dependencias fijadas a versiones conocidas. Añadidos `langchain-huggingface`, `langchain-core` y `python-dotenv`.
