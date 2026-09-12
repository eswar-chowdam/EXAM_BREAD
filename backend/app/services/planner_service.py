def build_study_plan_from_analysis(analysis: dict) -> dict:
    """Generate a topic-priority study plan from a completed exam analysis payload."""
    topics = analysis.get("topics", {})
    ranked_topics = sorted(
        topics.items(),
        key=lambda item: item[1].get("priority", item[1].get("count", 0) * 10),
        reverse=True,
    )

    days = []
    for index, (topic_name, details) in enumerate(ranked_topics[:7], start=1):
        questions = details.get("questions", []) or [f"Review {topic_name} concepts"]
        duration = 150 + (details.get("count", 0) * 20)
        learn = []

        if "Normalization" in topic_name:
            learn = ["1NF", "2NF", "3NF", "BCNF"]
        elif "SQL" in topic_name:
            learn = ["Inner Join", "Left Join", "Subqueries", "Aggregation"]
        elif "Transaction" in topic_name:
            learn = ["ACID", "Isolation levels", "Concurrency control", "Locks"]
        else:
            learn = ["Core definitions", "Examples", "Practice questions"]

        days.append(
            {
                "day": index,
                "topic": topic_name,
                "duration_minutes": duration,
                "learn": learn[:4],
                "practice": max(4, min(10, details.get("count", 0))),
                "quiz": max(5, min(12, details.get("count", 0) + 2)),
                "progress": 0,
                "questions": questions[:3],
            }
        )

    # Ensure exactly 7 days
    while len(days) < 7:
        day_num = len(days) + 1
        days.append(
            {
                "day": day_num,
                "topic": f"Comprehensive Revision {day_num - len(ranked_topics[:7])}",
                "duration_minutes": 120,
                "learn": ["Review all weak topics", "Mock Test Practice"],
                "practice": 10,
                "quiz": 15,
                "progress": 0,
                "questions": ["Complete a full mock exam."],
            }
        )

    return {
        "days": days,
        "study_window_days": len(days),
        "focus_summary": f"Prioritized from {analysis.get('total_questions', 0)} questions across {len(topics)} topic clusters.",
    }
