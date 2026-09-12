import re
from collections import defaultdict
import hashlib

from app.services.priority_engine import calculate_priority_score

TOPIC_RULES = {
    "Normalization": [
        "normalization",
        "1nf",
        "2nf",
        "3nf",
        "bcnf",
        "functional dependency",
        "dependency",
        "decomposition",
    ],
    "Transactions": [
        "acid",
        "transaction",
        "transactions",
        "isolation",
        "concurrency",
        "locking",
        "serializability",
    ],
    "SQL Joins": [
        "join",
        "left join",
        "right join",
        "inner join",
        "outer join",
        "natural join",
        "sql joins",
    ],
    "Indexes and Constraints": [
        "index",
        "constraint",
        "primary key",
        "foreign key",
        "unique key",
    ],
    "ER Modeling": [
        "er model",
        "entity relationship",
        "relationship",
        "attribute",
        "entity",
    ],
}


def extract_questions_from_text(text: str) -> list[str]:
    """Split raw PDF text into question-like entries using numbering heuristics."""
    if not text or not text.strip():
        return []

    cleaned = re.sub(r"\r\n", "\n", text)
    parts = re.split(r"\n\s*(?=\d+[\).\-]|Q\s*\d+|QUESTION\s*\d+)", cleaned)
    questions = []
    for part in parts:
        item = part.strip()
        if item and len(item) > 12:
            questions.append(item)
    return questions if questions else [cleaned.strip()]


def normalize_topic_name(name: str) -> str:
    raw = name.strip()
    if not raw:
        return "Uncategorized"

    normalized_parts = []
    for part in raw.split():
        if part.isupper() and len(part) > 1:
            normalized_parts.append(part)
        else:
            normalized_parts.append(part[:1].upper() + part[1:].lower())
    return " ".join(normalized_parts)


def infer_topic_from_question(question: str) -> str:
    if not question:
        return "General Concepts"
        
    patterns = [
        r"(?i)(?:explain|discuss|define|describe|what is|what are|write a short note on|write a note on|compare)\s+([a-zA-Z0-9\s\-]+?)(?:\?|\.|and|,|for|in|using|with|$)",
        r"(?i)(?:how does|how to|why is|why are)\s+([a-zA-Z0-9\s\-]+?)(?:\?|\.|and|,|for|in|using|with|$)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question)
        if match:
            topic = match.group(1).strip()
            if len(topic) > 2 and len(topic.split()) <= 4:
                return topic.title()
                
    caps = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', question)
    if caps:
        valid_caps = [c for c in caps if len(c) > 3]
        if valid_caps:
            return max(valid_caps, key=len).title()

    words = question.split()
    if len(words) > 2:
        return " ".join(words[:2]).title() + " Concepts"
    return "General Concepts"


def build_topic_summary(questions: list[dict]) -> dict[str, dict]:
    """Aggregate a list of question dicts by topic name and compute priority."""
    summary = defaultdict(lambda: {"count": 0, "questions": [], "priority": 0, "weakness": 0})

    for item in questions:
        question = item.get("question") or ""
        topic = normalize_topic_name(item.get("topic") or infer_topic_from_question(question))
        summary[topic]["count"] += 1
        summary[topic]["questions"].append(question)

    for topic, details in summary.items():
        # Scale count to 0-100 for frequency score
        frequency_score = min(100, details["count"] * 10)
        
        # Simulate stable pseudo-random weakness based on topic name for demo purposes
        hash_val = int(hashlib.md5(topic.encode()).hexdigest(), 16)
        weakness_score = 40 + (hash_val % 40)
        
        recency_score = 75
        marks_score = 60
        
        details["priority"] = calculate_priority_score(
            frequency_score=frequency_score,
            weakness_score=weakness_score,
            recency_score=recency_score,
            marks_score=marks_score
        )
        details["weakness"] = weakness_score

    return {topic: details for topic, details in summary.items()}


def analyze_exam_text(text: str) -> dict:
    """Turn raw exam copy into a structured topic summary used by the recommendation engine."""
    raw_questions = extract_questions_from_text(text)
    question_payload = []

    for question in raw_questions:
        topic = infer_topic_from_question(question)
        question_payload.append({
            "question": question.strip(),
            "topic": topic,
        })

    summary = build_topic_summary(question_payload)
    ranked_topics = sorted(summary.items(), key=lambda item: item[1]["priority"], reverse=True)

    return {
        "total_questions": len(question_payload),
        "questions": question_payload,
        "topics": summary,
        "most_frequent_topic": ranked_topics[0][0] if ranked_topics else "General DBMS",
    }
