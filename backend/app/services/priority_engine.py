def calculate_priority_score(
    frequency_score: float,
    weakness_score: float,
    recency_score: float,
    marks_score: float,
    weights: dict | None = None,
) -> float:
    """Compute a transparent 0-100 priority score.

    Default weights reflect the product requirement:
    frequency 0.40, weakness 0.35, recency 0.15, marks 0.10.
    """
    if weights is None:
        weights = {
            "frequency": 0.40,
            "weakness": 0.35,
            "recency": 0.15,
            "marks": 0.10,
        }

    score = (
        frequency_score * weights["frequency"]
        + weakness_score * weights["weakness"]
        + recency_score * weights["recency"]
        + marks_score * weights["marks"]
    )
    return round(score, 2)


def explain_priority_score(
    frequency_score: float,
    weakness_score: float,
    recency_score: float,
    marks_score: float,
    topic_name: str,
) -> dict:
    score = calculate_priority_score(
        frequency_score,
        weakness_score,
        recency_score,
        marks_score,
    )
    return {
        "topic": topic_name,
        "priority": score,
        "why": [
            "Appeared in multiple recent papers",
            "Your accuracy is below target",
            "Strong recent trend in history",
            "High marks contribution",
        ],
    }
