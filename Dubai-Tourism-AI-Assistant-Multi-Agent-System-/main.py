import json
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tourism_graph import build_tourism_graph, evaluate_system

app = FastAPI(title="Dubai Tourism AI Assistant")
graph = build_tourism_graph()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    intent: str
    response: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "live",
        "service": "Dubai Tourism AI Assistant",
        "version": "1.0.0",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    initial_state = {
        "user_query": request.query,
        "intent": "",
        "documents": [],
        "response": "",
    }
    result = graph.invoke(initial_state)
    return ChatResponse(
        intent=result.get("intent", "unknown"),
        response=result.get("response", "Sorry, I don't have information about that."),
    )


@app.get("/evaluate")
def run_evaluation():
    return {"metrics": evaluate_system()}


app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
