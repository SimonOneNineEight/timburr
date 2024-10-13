import logging
from sqlalchemy.orm import Session

from app.services.linkedin_scraper import scrape_jobs
from app.repositories.job_repository import JobRepository


def get_new_jobs(db: Session):
    scraped_jobs = scrape_jobs()

    existing_job_ids = JobRepository.get_all_job_posting_ids(db)

    if not scrape_jobs:
        logging.warning("No Job Scrapped!")
        return {"count": 0, "new_jobs": []}

    new_jobs = [
        job for job in scraped_jobs if job["job_posting_id"] not in existing_job_ids
    ]

    new_jobs = JobRepository.create_jobs(db, new_jobs)

    return {"count": len(new_jobs), "new_jobs": new_jobs}
