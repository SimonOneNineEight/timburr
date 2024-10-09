from sqlalchemy.orm import Session
from app.database.models import Job
from app.database.schemas import JobCreate


class JobRepository:
    @staticmethod
    def get_job(db: Session, job_id: int):
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 10):
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
        jobs_data = [Job(**job.model_dump()) for job in jobs]

        db.add_all(jobs_data)
        db.commit()
        db.refresh(jobs_data)

        return jobs_data
