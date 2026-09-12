from datetime import datetime

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class ExamPaper(Base):
    __tablename__ = "exam_papers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    year = Column(Integer, nullable=False)
    exam_date = Column(String, nullable=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="uploaded")
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    exam_paper_id = Column(Integer, ForeignKey("exam_papers.id"), nullable=False)
    year = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    source_page = Column(Integer, nullable=True)
    marks = Column(Integer, nullable=True)
    difficulty = Column(String, nullable=True)
    raw_source = Column(Text, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class QuestionTopic(Base):
    __tablename__ = "question_topics"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    confidence = Column(Float, default=0.0)


class StudentAttempt(Base):
    __tablename__ = "student_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    attempted = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    incorrect = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    time_taken_seconds = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class StudentTopicStat(Base):
    __tablename__ = "student_topic_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    attempted = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    incorrect = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    weakness_score = Column(Float, default=0.0)
    priority_score = Column(Float, default=0.0)
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    generated_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    exam_date = Column(String, nullable=True)
    starts_on = Column(String, nullable=True)
    status = Column(String, default="active")


class StudyTask(Base):
    __tablename__ = "study_tasks"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    task_type = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    completed = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    progress_percent = Column(Integer, default=0)
    due_date = Column(String, nullable=True)


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    started_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    completed_at = Column(String, nullable=True)
