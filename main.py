import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from tourism_graph import build_tourism_graph, evaluate_system, TourismState

app = FastAPI(title="Dubai Tourism AI Assistant")

graph = build_tourism_graph()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    intent: str
    response: str

@app.get("/health")
def health_check():
    """Health check endpoint — Render uses this to verify the app is alive."""
    return {
        "status": "live",
        "service": "Dubai Tourism AI Assistant",
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Send JSON body: {"query": "What are the best attractions in Dubai?"}
    """
    # Provide initial state matching TourismState
    initial_state = {
        "user_query": request.query,
        "intent": "",
        "documents": [],
        "response": ""
    }
    # Type ignore for Pylance
    result = graph.invoke(initial_state)  # type: ignore
    return ChatResponse(
        intent=result.get("intent", "unknown"),
        response=result.get("response", "Sorry, I don't have information about that.")
    )

@app.get("/evaluate")
def run_evaluation():
    """Run system evaluation and return metrics."""
    metrics = evaluate_system()
    return {"metrics": metrics}

# ── Local testing only ──
def main():
    test_queries = [
        "What are the best attractions to visit in Dubai?",
        "Can you recommend good restaurants in Dubai?",
        "Tell me about Dubai and the best time to visit.",
    ]
    for query in test_queries:
        print(f"\nUser: {query}")
        # Provide initial state matching TourismState
        initial_state: TourismState = {
            "user_query": query,
            "intent": "",
            "documents": [],
            "response": ""
        }
        result = graph.invoke(initial_state)
        print(f"Intent: {result['intent']}")
        print(f"Assistant: {result['response']}")
    print("\nEvaluation metrics:")
    print(json.dumps(evaluate_system(), indent=2))

if __name__ == "__main__":
    main()

# Mount static files after defining API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")