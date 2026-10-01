import json

from tourism_graph import build_tourism_graph, evaluate_system


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
