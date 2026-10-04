import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from tourism_graph import build_tourism_graph, evaluate_system, TourismState
from typing import Dict, Any, List

app = FastAPI(title='Dubai Tourism AI Assistant')

graph = build_tourism_graph()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    intent: str
    response: str

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Main chat endpoint.
    Send a JSON body :{"query": "What are the best attractions to visit in Dubai?"}
    """
    from tourism_graph import TourismState
    from typing import Dict, Any, List
    state: TourismState = {
        "user_query": request.query,
        "intent": "",
        "documents": [],  # type: List[Dict[str, Any]]
        "response": ""
    }
    result = graph.invoke(state)  # type: ignore
    return ChatResponse(
        intent=result.get("intent",'unknown'),
        response=result.get("response","Sorry, I don't have information about that. ")
    )

@app.get("/api/evaluate")
def run_evaluation():
    """Run system evaluation and return metrics"""
    metrics = evaluate_system()
    return {"metrics": metrics}

@app.get("/api/health")
def health_check():
    """Health check endpoint for Render"""
    return {
        "status": "live",
        "service": "Dubai Tourism AI Assistant",
        'version': '1.0.0'
    }

@app.get("/")
async def root():
    """Serve the main HTML page - UPDATED"""
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')

# Mount static files at /static path
app.mount("/static", StaticFiles(directory="static"), name="static")

def main():
    graph = build_tourism_graph()
    test_queries = [
        "What are the best attractions to visit in Dubai?",
        "Can you recommend good restaurants in Dubai?",
        "Tell me about Dubai and the best time to visit.",
    ]

    for query in test_queries:
        print(f"\nUser : {query}")
        from tourism_graph import TourismState
        from typing import Dict, Any, List
        state: TourismState = {
            "user_query": query,
            "intent": "",
            "documents": [],  # type: List[Dict[str, Any]]
            "response": ""
        }
        result = graph.invoke(state)
        print(f"Intent : {result['intent']}")
        print(f"Assistant : {result['response']}")

    print("\nEvaluation metrics:")
    print(json.dumps(evaluate_system(), indent=2))


if __name__ == '__main__':
    main()
