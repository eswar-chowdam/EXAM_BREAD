from fastapi.testclient import TestClient

from app.main import app
from app.services.planner_service import build_study_plan_from_analysis
from app.services.topic_analysis import analyze_exam_text, build_topic_summary, extract_questions_from_text

client = TestClient(app)


def test_extract_questions_from_text_splits_questions():
    text = "1. What is normalization?\n2. Explain ACID properties.\n3. What is a join?"

    questions = extract_questions_from_text(text)

    assert len(questions) == 3
    assert "normalization" in questions[0].lower()
    assert "acid" in questions[1].lower()


def test_build_topic_summary_counts_frequency():
    questions = [
        {"question": "Explain 1NF and 2NF", "topic": "Normalization"},
        {"question": "What is ACID property", "topic": "Transactions"},
        {"question": "Write a left join query", "topic": "SQL Joins"},
        {"question": "Discuss BCNF", "topic": "Normalization"},
    ]

    summary = build_topic_summary(questions)

    assert summary["Normalization"]["count"] == 2
    assert summary["Transactions"]["count"] == 1
    assert summary["SQL Joins"]["count"] == 1


def test_analyze_exam_text_builds_topic_summary_from_raw_questions():
    text = (
        "1. Explain 1NF, 2NF, and BCNF in DBMS.\n"
        "2. What are ACID properties?\n"
        "3. Write a left join query in SQL.\n"
        "4. Explain 1NF, 2NF, and BCNF again."
    )

    payload = analyze_exam_text(text)

    assert payload["total_questions"] == 4
    assert payload["topics"]["Normalization"]["count"] >= 2
    assert "SQL Joins" in payload["topics"]
    assert payload["most_frequent_topic"]


def test_pdf_processor_analyzes_generated_pdf_text(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length 120 >>\nstream\nBT\n/F1 12 Tf\n50 100 Td\n(1. Explain 1NF and BCNF.) Tj\nET\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000062 00000 n \n0000000122 00000 n \n0000000248 00000 n \n0000000590 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n655\n%%EOF"
    )

    from app.services.pdf_processor import analyze_pdf_file

    payload = analyze_pdf_file(pdf_path)

    assert payload["total_questions"] >= 1
    assert "Normalization" in payload["topics"]


def test_analysis_upload_endpoint_accepts_pdf_file(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length 120 >>\nstream\nBT\n/F1 12 Tf\n50 100 Td\n(1. Explain 1NF and BCNF.) Tj\nET\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000062 00000 n \n0000000122 00000 n \n0000000248 00000 n \n0000000590 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n655\n%%EOF"
    )

    with pdf_path.open("rb") as file_obj:
        response = client.post(
            "/api/analysis/upload",
            files={"file": ("sample.pdf", file_obj, "application/pdf")},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_questions"] >= 1
    assert "Normalization" in payload["topics"]


def test_build_study_plan_from_analysis_creates_real_topic_plan():
    analysis = {
        "topics": {
            "Normalization": {"count": 5, "questions": ["Explain 1NF", "Discuss BCNF"]},
            "SQL Joins": {"count": 4, "questions": ["Write a left join query"]},
            "Transactions": {"count": 3, "questions": ["What is ACID?", "What is isolation?"]},
        },
        "total_questions": 12,
    }

    plan = build_study_plan_from_analysis(analysis)

    assert len(plan["days"]) >= 3
    assert plan["days"][0]["topic"] == "Normalization"
    assert plan["days"][0]["duration_minutes"] > 0
    assert plan["days"][0]["learn"]
