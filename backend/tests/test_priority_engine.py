from app.services.priority_engine import calculate_priority_score


def test_priority_score_combines_frequency_weakness_recency_and_marks():
    score = calculate_priority_score(
        frequency_score=90,
        weakness_score=80,
        recency_score=70,
        marks_score=60,
    )

    assert score == 80.5
