# Dubai Tourism AI Assistant

A production-style tourism recommendation system built with Python, FastAPI, and LangGraph. The application classifies user intent, retrieves relevant Dubai travel content, and generates a polished response for attractions, restaurants, and general city information.

This project demonstrates a modular multi-agent workflow where each stage is responsible for a specific task: intent classification, document retrieval, and final response generation.

## Overview

Dubai Tourism AI Assistant helps travelers discover:

- Top attractions and landmarks in Dubai
- Recommended restaurants and dining experiences
- Helpful general information about Dubai and travel planning

The system combines a rule-based intent classification layer with a semantic retrieval pipeline using TF-IDF similarity scoring over curated tourism content. It is designed as a lightweight, explainable AI assistant that can be deployed as a web service.

## Key Features

- Intent classification for three categories:
  - Attractions
  - Restaurants
  - General information
- Retrieval-based tourism knowledge system with curated Dubai content
- LangGraph-based workflow orchestration
- FastAPI backend with REST API endpoints
- Static web front-end for local browsing
- Evaluation metrics for system performance
- Ready for deployment on Render or similar hosting platforms

## Architecture

The repository follows a simple, modular architecture:

- `main.py` – FastAPI application and API routes
- `tourism_graph.py` – stateful LangGraph workflow, intent routing, document retrieval, and response generation
- `static/` – front-end assets served by the application
- `tests/` – test scaffolding and validation logic
- `requirements.txt` – project dependencies
- `Procfile` – deployment configuration for Render

### Workflow

The application uses a graph-based state machine:

1. `classify_query` identifies the user intent
2. `retrieve_documents` filters or fetches relevant records from the Dubai knowledge base
3. `generate_response` formats the final answer for the user

This architecture makes the system easy to extend with more agents, more databases, or more advanced LLM-backed reasoning in the future.

## Tech Stack

- Python 3
- FastAPI
- LangGraph
- LangChain
- scikit-learn
- ChromaDB
- sentence-transformers
- Pydantic
- Uvicorn
- HTML / CSS / JavaScript frontend

## Repository Structure

```text
Dubai-Tourism-AI-Assistant-Multi-Agent-System-
├── .github/
├── static/
├── tests/
├── main.py
├── tourism_graph.py
├── index.html
├── Procfile
├── requirements.txt
├── README.md
├── TEST_SUMMARY.md
├── test_body.json
├── .gitignore
├── LICENSE
└── docs/
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Virtual environment tool (optional but recommended)

### Installation

```bash
git clone https://github.com/pradeesh-kumar-n/Dubai-Tourism-AI-Assistant-Multi-Agent-System-.git
cd Dubai-Tourism-AI-Assistant-Multi-Agent-System-
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Application

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- http://localhost:8000

## API Endpoints

### Health Check

```http
GET /health
```

Returns a simple service status payload:

```json
{
  "status": "live",
  "service": "Dubai Tourism AI Assistant",
  "version": "1.0.0"
}
```

### Chat Endpoint

```http
POST /chat
```

Request body:

```json
{
  "query": "What are the best attractions in Dubai?"
}
```

Response:

```json
{
  "intent": "attractions",
  "response": "Here are the best Dubai attractions matching your query: ..."
}
```

### Evaluation Endpoint

```http
GET /evaluate
```

Returns performance metrics such as route accuracy, retrieval hit rate, and latency values.

## Example Usage

### Using Python requests

```python
import requests

payload = {"query": "Recommend good restaurants in Dubai for brunch"}
response = requests.post("http://localhost:8000/chat", json=payload)
print(response.json())
```

### Using curl

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Tell me about Dubai and the best time to visit."}'
```

## Evaluation

The project includes a lightweight evaluation routine that tests the system against a set of human-like tourism queries. The `evaluate_system()` function measures:

- Route accuracy
- Retrieval hit rate
- Average latency
- p95 latency

This is useful for benchmarking intent routing and document selection logic as the project evolves.

## Deployment

The project is configured for deployment on Render using:

- `Procfile`
- `requirements.txt`
- Python application entrypoint in `main.py`

Example Render deployment steps:

1. Create a new Web Service in Render
2. Connect this repository
3. Use the default Python environment
4. Set the start command:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Notes

This project currently uses a retrieval-based, rule-informed architecture rather than a full LLM-powered travel agent. It is an excellent foundation for:

- integrating OpenAI or Azure OpenAI APIs
- adding multi-agent planning
- incorporating real-time location-aware recommendations
- extending the knowledge base with more Dubai attractions and dining venues

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome. If you would like to improve the assistant, consider:

- expanding the tourism data set
- improving intent detection accuracy
- adding richer user personalization
- enhancing the UI and conversational experience

## Author

Pradeesh Kumar N

## Acknowledgements

This project was designed to showcase the power of LangGraph orchestration, retrieval-based recommendation systems, and modular AI application design for domain-specific use cases.
