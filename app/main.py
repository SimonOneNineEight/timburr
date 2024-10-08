from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.database.db_connection import engine, SessionLocal, get_db, init_db
from app.database.schemas import JobCreate
from app.repositories.job_repository import JobRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init stage
    init_db()
    yield
    # shutdown stage


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return JobRepository.get_all_jobs(db)


@app.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        job_data = JobRepository.create_job(db, job)
        return job_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
