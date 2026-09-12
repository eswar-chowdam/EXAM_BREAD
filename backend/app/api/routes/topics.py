from fastapi import APIRouter

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/summary")
def topics_summary():
    return {
        "topics": [
            {
                "name": "Normalization",
                "frequency": 10,
                "years": [2022, 2023, 2024, 2025, 2026],
                "marks": 18,
                "trend": "Increasing",
                "accuracy": 42,
                "priority": 94,
                "status": "Critical"
            },
            {
                "name": "SQL Joins",
                "frequency": 9,
                "years": [2022, 2023, 2024, 2025],
                "marks": 14,
                "trend": "Stable",
                "accuracy": 87,
                "priority": 72,
                "status": "High Priority"
            },
            {
                "name": "Transactions",
                "frequency": 7,
                "years": [2023, 2024, 2025, 2026],
                "marks": 12,
                "trend": "Strong recent trend",
                "accuracy": 48,
                "priority": 81,
                "status": "Critical"
            }
        ]
    }
