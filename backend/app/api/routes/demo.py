from fastapi import APIRouter

from app.services.demo_dataset import build_demo_dbms_dataset

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/dbms")
def load_demo_dbms():
    payload = build_demo_dbms_dataset()
    return {
        "subject": payload["subject"],
        "message": "Demo DBMS dataset loaded successfully.",
        "stats": {
            "years_analyzed": payload["years_analyzed"],
            "questions_detected": payload["questions_detected"],
            "topics_identified": payload["topics_identified"],
            "plan_length_days": 7,
        },
        "top_topics": [
            {"topic": topic["name"], "frequency": topic["frequency"], "priority": topic["priority"]}
            for topic in payload["topic_intelligence"]
        ],
        "data": payload,
    }
