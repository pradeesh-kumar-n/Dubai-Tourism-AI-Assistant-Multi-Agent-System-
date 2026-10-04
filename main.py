import json
from fastapi import FastAPI
from pydantic import BaseModel
from tourism_graph import build_tourism_graph, evaluate_system

app=FastAPI(title='Dubai Tourism  AI Assistant')
graph =build_tourism_graph()

class ChatRequest(BaseModel):
    query :str
class ChatResponse(BaseModel):
    intent:str
    response:str
@app.get('/')
def health_check():
    """Root endpoint-Render uses this to check if your app is alive"""
    return {
        "status":"live",
        "service":"Dubai Tourism AI Assistant",
        'version': '1.0.0'
    }
@app.post('/chat', response_model=ChatResponse)
def  chat(request: ChatRequest):
    """Main chat endpoint.
    Send a JSON body :{"query": "What are the best attractions to visit in Dubai?"}
    """
    result=graph.invoke({"user_query":request.query})
    return ChatResponse(
        intent=result.get("intent",'unknown'),
        response=result.get("response","Sorry, I don't have information about that. ")
    )
@app.get('/evaluate')
def run_evaluation():
    """Run system evaluation and return metrics"""
    metrics =evaluate_system()
    return {"metrics":metrics}

def main():
    graph = build_tourism_graph()
    test_queries = [
        "What are the best attractions to visit in Dubai?",
        "Can you recommend good restaurants in Dubai?",
        "Tell me about Dubai and the best time to visit.",
    ]

    for query in test_queries:
        print(f"\nUser : {query}")
        result = graph.invoke({"user_query": query})
        print(f"Intent : {result['intent']}")
        print(f"Assistant : {result['response']}")

    print("\nEvaluation metrics:")
    print(json.dumps(evaluate_system(), indent=2))


if __name__ == '__main__':
    main()
