from pydamic import BaseModel
from datetime import date


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    job_posting_id: str
    job_url: str
    date: date
    job_description: str
