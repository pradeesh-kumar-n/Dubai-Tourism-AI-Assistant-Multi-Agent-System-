from tourism_graph import build_tourism_graph

def main():
    graph = build_tourism_graph()
    test_queries = [
        "What are the best attractions to visit?",
        "Can you recommend good restaurants?",
        "Tell me about Dubai"
    ]
    for query in test_queries:
        print(f"\nUser : {query}")
        result = graph.invoke({"user_query": query})
        print(f"\nAssistant : {result['response']}")

if __name__ == '__main__':
    main()
