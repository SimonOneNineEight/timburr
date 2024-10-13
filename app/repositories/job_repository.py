from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.models import Job
from app.database.schemas import JobCreate


class JobRepository:
    @staticmethod
    def get_job(db: Session, job_id: int):
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Job).offset(skip).limit(limit).all()

    @staticmethod
    def create_job(db: Session, job: JobCreate):
        db_job = Job(**job.model_dump())

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return db_job

    @staticmethod
    def create_jobs(db: Session, jobs: list[JobCreate]):
        print("Start creating")
        jobs_data = []
        for job in jobs:
            if isinstance(job, BaseModel):
                jobs_data.append(Job(**job.model_dump()))
            else:
                jobs_data.append(Job(**job))

        db.add_all(jobs_data)
        db.commit()
        # db.refresh(jobs_data)

        return jobs_data

    @staticmethod
    def get_all_job_posting_ids(db):
        job_posting_ids = db.query(Job.job_posting_id).all()
        return job_posting_ids
