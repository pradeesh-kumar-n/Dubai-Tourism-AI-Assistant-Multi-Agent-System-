import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from tourism_graph import build_tourism_graph, evaluate_system

app = FastAPI(title='Dubai Tourism AI Assistant')

# Serve static files at ROOT so UI opens at https://your-app.onrender.com/
# Health check moved to /health to avoid conflict
app.mount('/', StaticFiles(directory='static', html=True), name='static')

graph = build_tourism_graph()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    intent: str
    response: str

@app.get('/health')
def health_check():
    return {
        'status': 'live',
        'service': 'Dubai Tourism AI Assistant',
        'version': '1.0.0'
    }

@app.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest):
    result = graph.invoke({'user_query': request.query})
    return ChatResponse(
        intent=result.get('intent', 'unknown'),
        response=result.get('response', 'Sorry, I don\'t have information about that.')
    )

@app.get('/evaluate')
def run_evaluation():
    metrics = evaluate_system()
    return {'metrics': metrics}

# Local testing only
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
