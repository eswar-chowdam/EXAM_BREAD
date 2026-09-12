# EXAM BREAD

A premium exam-preparation intelligence platform that analyzes previous-year question papers (PYQs), identifies topic patterns, reveals weak areas, and generates a personalized 7-day study plan.

## Overview

EXAM BREAD helps students focus on what matters instead of trying to cover everything. The platform ingests multiple years of exam papers, extracts questions, groups them into topic clusters, calculates topic frequency and importance, measures the student’s relative weakness, and builds an adaptive study recipe around the highest-value learning needs.

## Problem Statement

Students often study from broad syllabi without understanding which topics are historically emphasized in exams. This causes inefficient preparation, weak prioritization, and poor exam performance.

## Solution

The platform combines:

- PDF question extraction and cleaning
- Topic modeling and clustering
- Historical frequency analysis
- Student weakness analysis
- Transparent priority scoring
- Adaptive 7-day personalization

This produces a study plan that reflects both exam trends and the student’s actual needs.

## Architecture

```text
Frontend (React + Vite + Tailwind)
    |
    v
API Layer (FastAPI)
    |
    +--> PDF Processing / Question Extraction
    +--> Topic Intelligence Engine
    +--> Frequency Analysis Engine
    +--> Weakness Engine
    +--> Priority Engine
    +--> Study Planner
    |
    v
Database (SQLite/PostgreSQL)
```

## Features

- Multi-PDF upload and validation
- PDF text extraction and question parsing
- Topic clustering and trend analysis
- Student performance tracking
- Priority scoring with explainability
- 7-day adaptive study plan
- Practice quiz flow
- Dashboard and readiness score
- Demo mode for quick visualization

## Tech Stack

- Frontend: React, Vite, Tailwind CSS, Recharts
- Backend: Python, FastAPI
- Database: PostgreSQL / SQLite
- PDF processing: PyMuPDF or pdfplumber
- ML / NLP: scikit-learn, sentence-transformers (optional)
- Auth: JWT + bcrypt

## Database Design

Planned relational tables include:

- users
- subjects
- exam_papers
- questions
- topics
- question_topics
- student_attempts
- student_topic_stats
- study_plans
- study_tasks
- bookmarks
- quiz_sessions

## Algorithm Explanation

The recommendation system uses a weighted formula such as:

Priority Score = Frequency × 0.40 + Weakness × 0.35 + Recency × 0.15 + Marks Importance × 0.10

This supports explainability and transparent recommendations rather than opaque ranking.

## Installation

1. Clone the repository.
2. Set up the frontend environment.
3. Set up the backend environment.
4. Configure environment variables.
5. Run migrations and start the app.

## Environment Variables

See .env.example for expected configuration.

## Running Locally

Frontend:

npm install
npm run dev

Backend:

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Screenshots

Screenshots will be added later as the app matures.

## Future Improvements

- Better semantic topic classification using local embeddings
- More robust OCR for scanned PDFs
- LMS-style analytics and cohort insights
- Collaboration and mentor review
- Deep exam prediction modeling with safeguards

## License

Project is intended for hackathon/demo use and is not yet production-licensed.
