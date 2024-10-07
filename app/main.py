from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.database.models import Base
from app.database.db_connection import engine, SessionLocal, get_db
from app.repositories.job_repository import JobRepository
from config import settings

engine = create_engine(settings.DATABASE_URL)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return JobRepository.get_all_jobs(db)
