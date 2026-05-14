def classify_query(query: str) -> str:
    """
    Classify whether query is simple or complex
    Simple = direct factual retrieval
    Complex = analysis, comparison, reasoning
    """

    query = query.lower()

    complex_keywords = [
        "compare",
        "difference",
        "analyze",
        "why",
        "impact",
        "risk",
        "evaluate",
        "advantages",
        "disadvantages",
        "strategy"
    ]

    for keyword in complex_keywords:
        if keyword in query:
            return "complex"

    return "simple"