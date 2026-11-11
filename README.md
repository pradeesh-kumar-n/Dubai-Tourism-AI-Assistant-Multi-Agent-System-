# Dubai Tourism AI Assistant

A lightweight Dubai tourism recommendation app with a FastAPI backend and a simple static frontend.

## Features
- Route travel questions into `attractions`, `restaurants`, or `general`
- Return curated Dubai recommendations based on the app's knowledge base
- Expose `/health` and `/chat` for deployment and testing
- Serve a simple web UI from the `static/` folder

## Run locally
```bash
git clone https://github.com/pradeesh-kumar-n/Dubai-Tourism-AI-Assistant-Multi-Agent-System-.git
cd Dubai-Tourism-AI-Assistant-Multi-Agent-System-
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open:
- http://localhost:8000
- http://localhost:8000/docs

## API
### Health check
```bash
curl http://localhost:8000/health
```

### Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What are the best attractions in Dubai?"}'
```

## Deploy on Render
1. Connect this repository to Render as a Web Service.
2. Use the start command:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
3. Set the build command:
```bash
pip install -r requirements.txt
```
4. Keep the app root at the repository root.

This project is ready for a standard Python Render deployment.
