from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Case


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="OpsGenome AI API",
    version="0.1.0",
    lifespan=lifespan,
)


def get_db():
    with SessionLocal() as db:
        yield db


DBSession = Annotated[Session, Depends(get_db)]


class CaseCreate(BaseModel):
    external_id: str | None = None
    title: str
    description: str | None = None
    status: str = "open"
    assigned_to: str | None = None
    outcome: str | None = None


class CaseResponse(CaseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "opsgenome-api"}


@app.get("/health/db")
def database_health(db: DBSession):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from exc


@app.post("/cases", response_model=CaseResponse, status_code=201)
def create_case(payload: CaseCreate, db: DBSession):
    case = Case(**payload.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@app.get("/cases", response_model=list[CaseResponse])
def list_cases(db: DBSession):
    return db.scalars(
        select(Case).order_by(Case.id.desc())
    ).all()