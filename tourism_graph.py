from __future__ import annotations

import json
import time
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ATTRACTIONS = [
    {
        "id": "burj_khalifa",
        "category": "attractions",
        "title": "Burj Khalifa",
        "summary": "The tallest building in the world, with observation decks overlooking Dubai's skyline and desert horizon.",
        "keywords": ["burj khalifa", "tower", "skyline", "observation deck", "views"],
    },
    {
        "id": "dubai_marina",
        "category": "attractions",
        "title": "Dubai Marina",
        "summary": "A modern waterfront district with yachts, cafes, and walking promenades near luxury hotels.",
        "keywords": ["dubai marina", "waterfront", "yachts", "promenade", "nightlife"],
    },
    {
        "id": "palm_jumeirah",
        "category": "attractions",
        "title": "Palm Jumeirah",
        "summary": "A man-made island known for luxury resorts, beach clubs, and stunning sea views.",
        "keywords": ["palm jumeirah", "beach", "resort", "island", "sea views"],
    },
    {
        "id": "desert_safari",
        "category": "attractions",
        "title": "Desert Safari",
        "summary": "An adventurous excursion including dune bashing, cultural performances, and Bedouin-style dining.",
        "keywords": ["desert safari", "dunes", "adventure", "camp", "outdoor"],
    },
    {
        "id": "dubai_creek",
        "category": "attractions",
        "title": "Dubai Creek",
        "summary": "A historic district linking old Dubai with the modern city through heritage souks and waterfront walks.",
        "keywords": ["dubai creek", "historic", "heritage", "souk", "old dubai"],
    },
]

RESTAURANTS = [
    {
        "id": "pierchic",
        "category": "restaurants",
        "title": "Pierchic",
        "summary": "A waterfront seafood restaurant with iconic views over the Arabian Gulf and romantic sunset dining.",
        "keywords": ["seafood", "seafood restaurant", "sunset", "romantic", "waterfront"],
    },
    {
        "id": "al_hadheerah",
        "category": "restaurants",
        "title": "Al Hadheerah",
        "summary": "A destination dining experience with live entertainment, desert atmosphere, and premium Emirati menus.",
        "keywords": ["desert dining", "arabic food", "dinner", "entertainment", "emirati"],
    },
    {
        "id": "the_green_room",
        "category": "restaurants",
        "title": "The Green Room",
        "summary": "A stylish lounge and dining venue serving international cuisine in a relaxed, upscale atmosphere.",
        "keywords": ["international cuisine", "lounge", "brunch", "dinner", "upscale"],
    },
    {
        "id": "ministry_of_desserts",
        "category": "restaurants",
        "title": "Ministry of Desserts",
        "summary": "A dessert-focused concept known for indulgent sweet plates and creative, Instagram-worthy presentation.",
        "keywords": ["dessert", "sweets", "cake", "sweet", "brunch"]
    },
    {
        "id": "buddha_bar",
        "category": "restaurants",
        "title": "Buddha-Bar Dubai",
        "summary": "A chic restaurant blending Asian-inspired dishes with elevated nightlife energy and skyline views.",
        "keywords": ["asian food", "nightlife", "cocktails", "fine dining", "stylish"],
    },
]

GENERAL_INFO = [
    {
        "id": "dubai_overview",
        "category": "general",
        "title": "Dubai Overview",
        "summary": "Dubai is a major city in the UAE known for luxury shopping, futuristic architecture, and diverse visitor experiences.",
        "keywords": ["dubai", "uae", "city", "travel", "overview"],
    },
    {
        "id": "uae_travel_tips",
        "category": "general",
        "title": "UAE Travel Tips",
        "summary": "Visitors can combine modern city attractions with cultural heritage, family-friendly experiences, and desert escapes.",
        "keywords": ["travel tips", "uae", "culture", "family", "advice"],
    },
    {
        "id": "best_time_to_visit",
        "category": "general",
        "title": "Best Time to Visit",
        "summary": "The cooler months from November to March are most comfortable for outdoor sightseeing and waterfront activities.",
        "keywords": ["weather", "travel season", "summer", "winter", "best time"],
    },
]

DOCS = ATTRACTIONS + RESTAURANTS + GENERAL_INFO

def _build_index():
    text_blocks = [
        f"{doc['title']} {' '.join(doc['keywords'])} {doc['summary']}" for doc in DOCS
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(text_blocks)
    return vectorizer, matrix


VECTORIZER, INDEX_MATRIX = _build_index()


class TourismState(TypedDict):
    user_query: str
    intent: str
    documents: List[Dict[str, Any]]
    response: str


def classify_query(query: str) -> str:
    lower = query.lower()

    attraction_signals = [
        "burj khalifa", "palm jumeirah", "dubai marina", "dubai creek",
        "attraction", "attractions", "things to do", "places to visit", "places",
        "tour", "landmark", "sightseeing", "museum", "beach", "marina", "desert",
        "creek", "do in dubai", "visit dubai", "visit the"
    ]
    general_signals = [
        "tell me about", "what is", "overview", "uae tourism", "travel in dubai",
        "first-time visitors", "best time to visit", "before traveling", "what should i know",
        "how is travel", "travel tips", "weather", "season", "tourism"
    ]
    restaurant_signals = [
        "restaurant", "restaurants", "eat", "eating", "dine", "dining", "food",
        "brunch", "lunch", "dinner", "cafe", "cuisine", "seafood", "dessert"
    ]

    if any(signal in lower for signal in attraction_signals):
        return "attractions"
    if any(signal in lower for signal in general_signals):
        return "general"
    if any(signal in lower for signal in restaurant_signals):
        return "restaurants"
    return "general"


def retrieve_documents(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    query_text = VECTORIZER.transform([query])
    similarities = cosine_similarity(query_text, INDEX_MATRIX).ravel()
    ranked_indices = similarities.argsort()[-top_k:][::-1]
    ranked_docs = [DOCS[index] for index in ranked_indices if similarities[index] > 0]

    if not ranked_docs:
        return DOCS[:top_k]
    return ranked_docs


def filter_documents_by_intent(intent: str, query: str) -> List[Dict[str, Any]]:
    candidates = [doc for doc in DOCS if doc["category"] == intent]
    if not candidates:
        return DOCS[:3]
    if intent == "general":
        return candidates[:3]
    q = query.lower()
    preferred = []
    for doc in candidates:
        if any(keyword in q for keyword in doc["keywords"]):
            preferred.append(doc)
    if preferred:
        return preferred[:3]
    return candidates[:3]


def _compose_response(intent: str, query: str, documents: List[Dict[str, Any]]) -> str:
    if intent == "attractions":
        intro = "Here are the best Dubai attractions matching your query:"
    elif intent == "restaurants":
        intro = "Here are the most relevant Dubai dining options:"
    else:
        intro = "Here is a concise overview of Dubai for your question:"

    bullet_lines = []
    for doc in documents[:3]:
        bullet_lines.append(f"- {doc['title']}: {doc['summary']}")

    if not bullet_lines:
        return f"{intro}\n- I couldn't find a strong match, but Dubai is known for a mix of luxury experiences, heritage sites, and waterfront dining."

    return f"{intro}\n" + "\n".join(bullet_lines)


def classify_query_node(state: TourismState) -> TourismState:
    state["intent"] = classify_query(state["user_query"])
    return state


def retrieve_documents_node(state: TourismState) -> TourismState:
    if state["intent"] in {"attractions", "restaurants", "general"}:
        docs = filter_documents_by_intent(state["intent"], state["user_query"])
    else:
        docs = retrieve_documents(state["user_query"])
    state["documents"] = docs
    return state


def generate_response_node(state: TourismState) -> TourismState:
    docs = state.get("documents") or retrieve_documents(state["user_query"])
    state["response"] = _compose_response(state["intent"], state["user_query"], docs)
    return state


def build_tourism_graph():
    graph = StateGraph(TourismState)
    graph.add_node("classify_query", classify_query_node)
    graph.add_node("retrieve_documents", retrieve_documents_node)
    graph.add_node("generate_response", generate_response_node)

    graph.add_edge(START, "classify_query")
    graph.add_conditional_edges(
        "classify_query",
        lambda state: state["intent"],
        {
            "attractions": "retrieve_documents",
            "restaurants": "retrieve_documents",
            "general": "retrieve_documents",
        },
    )
    graph.add_edge("retrieve_documents", "generate_response")
    graph.add_edge("generate_response", END)
    return graph.compile()


def evaluate_system() -> Dict[str, Any]:
    graph = build_tourism_graph()
    test_queries = [
        ("What are the best attractions to visit in Dubai?", "attractions"),
        ("Recommend top tourist places in Dubai Marina.", "attractions"),
        ("Tell me about the Burj Khalifa experience.", "attractions"),
        ("What should I do in Dubai for a family trip?", "attractions"),
        ("I want to visit the Palm Jumeirah and Dubai Creek.", "attractions"),
        ("Where can I eat seafood in Dubai?", "restaurants"),
        ("What are the best restaurants in Dubai for sunset dining?", "restaurants"),
        ("Recommend some good dining spots in Dubai for brunch.", "restaurants"),
        ("Which are the best dessert places in Dubai?", "restaurants"),
        ("I want an upscale restaurant with nightlife views.", "restaurants"),
        ("Tell me about Dubai.", "general"),
        ("What is the best time to visit the UAE?", "general"),
        ("How is travel in Dubai for first-time visitors?", "general"),
        ("Give me an overview of UAE tourism.", "general"),
        ("What should I know before traveling to Dubai?", "general"),
    ]

    route_correct = 0
    retrieval_correct = 0
    latencies = []

    for query, expected_intent in test_queries:
        start = time.perf_counter()
        result = graph.invoke({"user_query": query})
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)

        if result["intent"] == expected_intent:
            route_correct += 1

        found_match = any(doc["category"] == expected_intent for doc in result.get("documents", []))
        if found_match:
            retrieval_correct += 1

    metrics = {
        "query_count": len(test_queries),
        "route_accuracy": round(route_correct / len(test_queries), 4),
        "retrieval_hit_rate_at_3": round(retrieval_correct / len(test_queries), 4),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "p95_latency_ms": round(sorted(latencies)[int(0.95 * len(latencies)) - 1], 2),
        "examples": [
            {"query": query, "expected": expected_intent, "predicted": graph.invoke({"user_query": query})["intent"]}
            for query, expected_intent in test_queries[:3]
        ],
    }
    return metrics


if __name__ == "__main__":
    graph = build_tourism_graph()
    sample_queries = [
        "What are the best attractions to visit?",
        "Can you recommend good restaurants?",
        "Tell me about Dubai",
    ]

    for query in sample_queries:
        print(f"\nUser: {query}")
        result = graph.invoke({"user_query": query})
        print(f"Intent: {result['intent']}")
        print(result["response"])

    print("\nEvaluation metrics:")
    print(json.dumps(evaluate_system(), indent=2))
