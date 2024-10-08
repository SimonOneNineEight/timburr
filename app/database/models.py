from sqlalchemy import Column, Integer, String, Date, Boolean, event
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, UTC

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    job_posting_id = Column(String, index=True)
    job_url = Column(String)
    date = Column(Date, index=True)
    job_description = Column(String)
    is_applied = Column(Boolean)
    apply_status = Column(String)
    is_offered = Column(Boolean)


@event.listens_for(Job, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = datetime.now(UTC)
    target.updated_at = datetime.now(UTC)


@event.listens_for(Job, "before_update")
def set_created_at(mapper, connection, target):
    target.updated_at = datetime.now(UTC)
