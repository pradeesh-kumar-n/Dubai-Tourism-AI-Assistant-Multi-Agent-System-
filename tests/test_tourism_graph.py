from tourism_graph import build_tourism_graph, evaluate_system


def test_build_tourism_graph_routes_attraction_queries():
    graph = build_tourism_graph()
    result = graph.invoke({"user_query": "What are the best attractions to visit in Dubai?"})

    assert result["intent"] == "attractions"
    assert "Burj Khalifa" in result["response"] or "Dubai Marina" in result["response"]


def test_evaluate_system_reports_metrics():
    metrics = evaluate_system()

    assert metrics["route_accuracy"] >= 0.75
    assert metrics["retrieval_hit_rate_at_3"] >= 0.75
