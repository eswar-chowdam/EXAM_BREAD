from datetime import datetime

from fastapi import APIRouter, Depends, Request, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import ExamPaper, Subject, User
from app.services.auth_service import get_current_user_optional
from app.services.pdf_processor import analyze_pdf_file
from app.services.topic_analysis import analyze_exam_text

router = APIRouter(prefix="/analysis", tags=["analysis"])


class AnalyzeTextRequest(BaseModel):
    text: str


@router.get("/status")
def analysis_status():
    return {
        "status": "ready",
        "phase": "paper ingestion",
        "progress": 20,
        "message": "Analyzing your exam history...",
    }


@router.post("/text")
def analyze_text(payload: AnalyzeTextRequest):
    if not payload.text or not payload.text.strip():
        return {
            "total_questions": 0,
            "questions": [],
            "topics": {},
            "most_frequent_topic": "General Concepts",
            "message": "No text provided for analysis.",
        }

    return {
        **analyze_exam_text(payload.text),
        "message": "Exam text processed successfully.",
    }


@router.post("/upload")
async def upload_and_analyze(
    request: Request,
    file: UploadFile,
    db: Session = Depends(get_db),
):
    current_user = get_current_user_optional(request, db)
    if not file or not file.filename:
        return {
            "total_questions": 0,
            "questions": [],
            "topics": {},
            "most_frequent_topic": "General DBMS",
            "message": "No file uploaded.",
        }

    import tempfile

    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        temp_path = tmp.name

    try:
        payload = analyze_pdf_file(temp_path)

        subject_name = "DBMS"
        subject = db.query(Subject).filter(Subject.name == subject_name).first()
        if not subject:
            subject = Subject(name=subject_name, code="DBMS")
            db.add(subject)
            db.commit()
            db.refresh(subject)

        paper_id = None
        if current_user is not None:
            paper = ExamPaper(
                user_id=current_user.id,
                subject_id=subject.id,
                year=datetime.now().year,
                exam_date=datetime.now().strftime("%Y-%m-%d"),
                file_name=file.filename,
                file_path=temp_path,
                status="analyzed",
            )
            db.add(paper)
            db.commit()
            db.refresh(paper)
            paper_id = paper.id

        return {
            **payload,
            "paper_id": paper_id,
            "subject": subject_name,
            "message": f"File {file.filename} analyzed successfully.",
        }
    finally:
        try:
            import os
            os.remove(temp_path)
        except FileNotFoundError:
            pass


@router.get("/history")
def get_analysis_history(
    request: Request,
    db: Session = Depends(get_db),
):
    current_user = get_current_user_optional(request, db)
    if current_user is None:
        return {"items": []}
    papers = (
        db.query(ExamPaper)
        .filter(ExamPaper.user_id == current_user.id)
        .order_by(ExamPaper.created_at.desc())
        .all()
    )

    return {
        "items": [
            {
                "id": paper.id,
                "file_name": paper.file_name,
                "status": paper.status,
                "year": paper.year,
                "exam_date": paper.exam_date,
                "created_at": paper.created_at,
            }
            for paper in papers
        ]
    }


@router.post("/save")
def save_analysis_result(
    request: Request,
    payload: dict,
    db: Session = Depends(get_db),
):
    current_user = get_current_user_optional(request, db)
    if current_user is None:
        return {"status": "saved", "subject": str(payload.get("subject") or "DBMS"), "message": "Analysis saved for guest session."}
    subject_name = str(payload.get("subject") or "DBMS")
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        subject = Subject(name=subject_name, code=subject_name.upper())
        db.add(subject)
        db.commit()
        db.refresh(subject)

    paper = ExamPaper(
        user_id=current_user.id,
        subject_id=subject.id,
        year=int(payload.get("year") or datetime.now().year),
        exam_date=str(payload.get("exam_date") or datetime.now().strftime("%Y-%m-%d")),
        file_name=str(payload.get("file_name") or f"{subject_name}-analysis.pdf"),
        file_path=str(payload.get("file_path") or "uploaded"),
        status="saved",
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)

    return {
        "paper_id": paper.id,
        "status": "saved",
        "subject": subject_name,
        "message": "Analysis saved to your account.",
    }
