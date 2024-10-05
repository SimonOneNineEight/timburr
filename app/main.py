from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.database.models import Base
from app.database.db_connection import engine, SessionLocal, get_db 

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

