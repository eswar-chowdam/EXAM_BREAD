from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import StudyPlan, StudyTask, Subject, Topic, User
from app.services.auth_service import get_current_user
from app.services.planner_service import build_study_plan_from_analysis

router = APIRouter(prefix="/planner", tags=["planner"])


class AnalysisPlanRequest(BaseModel):
    analysis: dict


@router.get("/sample-plan")
def sample_plan():
    return {
        "days": [
            {
                "day": 1,
                "topic": "Normalization",
                "duration_minutes": 210,
                "learn": ["1NF", "2NF", "3NF", "BCNF"],
                "practice": 8,
                "quiz": 10,
                "progress": 0,
            },
            {
                "day": 2,
                "topic": "Transactions",
                "duration_minutes": 180,
                "learn": ["ACID", "Isolation levels", "Concurrency control"],
                "practice": 7,
                "quiz": 9,
                "progress": 0,
            },
            {
                "day": 3,
                "topic": "SQL Joins",
                "duration_minutes": 200,
                "learn": ["Inner Join", "Left Join", "Subqueries"],
                "practice": 8,
                "quiz": 10,
                "progress": 0,
            }
        ]
    }


@router.post("/from-analysis")
def plan_from_analysis(
    payload: AnalysisPlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = build_study_plan_from_analysis(payload.analysis)

    subject_name = "DBMS"
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        subject = Subject(name=subject_name, code="DBMS")
        db.add(subject)
        db.commit()
        db.refresh(subject)

    study_plan = StudyPlan(
        user_id=current_user.id,
        subject_id=subject.id,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        exam_date=datetime.now().strftime("%Y-%m-%d"),
        starts_on=datetime.now().strftime("%Y-%m-%d"),
        status="active",
    )
    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)

    for day in plan.get("days", [])[:7]:
        topic_name = day.get("topic") or "General DBMS"
        topic = db.query(Topic).filter(Topic.name == topic_name, Topic.subject_id == subject.id).first()
        if not topic:
            topic = Topic(subject_id=subject.id, name=topic_name, description="Generated from exam analysis")
            db.add(topic)
            db.commit()
            db.refresh(topic)

        task = StudyTask(
            plan_id=study_plan.id,
            topic_id=topic.id,
            day_number=day.get("day", 1),
            task_type="study",
            duration_minutes=int(day.get("duration_minutes") or 120),
            title=f"{topic_name} revision",
            details="Auto-generated from topic priority analysis.",
            completed=0,
            skipped=0,
            progress_percent=0,
        )
        db.add(task)

    db.commit()
    plan["plan_id"] = study_plan.id
    return plan


@router.get("/history")
def get_plan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plans = (
        db.query(StudyPlan)
        .filter(StudyPlan.user_id == current_user.id)
        .order_by(StudyPlan.generated_at.desc())
        .all()
    )

    return {
        "items": [
            {
                "id": plan.id,
                "status": plan.status,
                "starts_on": plan.starts_on,
                "exam_date": plan.exam_date,
                "generated_at": plan.generated_at,
            }
            for plan in plans
        ]
    }
