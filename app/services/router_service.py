
# version 1 for onlu 2 llm 
# def classify_query(query: str) -> str:
#     """
#     Classify whether query is simple or complex
#     Simple = direct factual retrieval
#     Complex = analysis, comparison, reasoning
#     """

#     query = query.lower()

#     complex_keywords = [
#         "compare",
#         "difference",
#         "analyze",
#         "why",
#         "impact",
#         "risk",
#         "evaluate",
#         "advantages",
#         "disadvantages",
#         "strategy"
#     ]

#     for keyword in complex_keywords:
#         if keyword in query:
#             return "complex"

#     return "simple"

# version 2 with 3 levels of classification
def classify_query(query: str) -> str:
    """
    Router v2:
    simple   = direct retrieval
    moderate = explanation/comparison
    complex  = strategic/deep analysis
    """

    query = query.lower()

    complex_keywords = [
        "strategy",
        "architecture",
        "deep analysis",
        "evaluate",
        "long-term impact"
    ]

    moderate_keywords = [
        "compare",
        "difference",
        "analyze",
        "why",
        "impact",
        "risk",
        "advantages",
        "disadvantages"
    ]

    # Complex first
    for keyword in complex_keywords:
        if keyword in query:
            return "complex"

    # Moderate second
    for keyword in moderate_keywords:
        if keyword in query:
            return "moderate"

    return "simple"