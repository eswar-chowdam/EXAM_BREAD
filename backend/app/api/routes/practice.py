from fastapi import APIRouter

router = APIRouter(prefix="/practice", tags=["practice"])


@router.get("/sample-question")
def sample_question():
    return {
        "question": "Which normal form removes partial dependency?",
        "options": ["1NF", "2NF", "3NF", "BCNF"],
        "correct_index": 1,
        "explanation": "2NF removes partial dependency by ensuring every non-key attribute depends on the whole key.",
        "topic": "Normalization",
        "difficulty": "Medium",
        "source_year": 2024,
        "source_label": "DBMS 2024 PYQ"
    }
