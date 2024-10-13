from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_connection import engine, SessionLocal, get_db, init_db
from app.database.schemas import JobCreate
from app.repositories.job_repository import JobRepository
from app.services.job_services import get_new_jobs

router = APIRouter()

@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return JobRepository.get_all_jobs(db)


@router.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        job_data = JobRepository.create_job(db, job)
        return job_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sync-new-jobs")
def sync_new_jobs(db: Session = Depends(get_db)):
    try:
        result = get_new_jobs(db)
        return {"message": f"Scraped {result["count"]} job posts and stored complete!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
