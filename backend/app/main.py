from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analysis, auth, demo, health, planner, practice, topics
from app.db.database import init_db

app = FastAPI(title="EXAM BREAD API", version="1.0.0")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(demo.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(planner.router, prefix="/api")
app.include_router(topics.router, prefix="/api")
app.include_router(practice.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/")
def read_root():
    return {"service": "EXAM BREAD", "status": "online"}
