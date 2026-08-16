import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session, select

# ── Database Setup ─────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./school.db")

# Neon / Heroku sometimes returns postgres:// — SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)


# ── SQLModel Tables ────────────────────────────────────────────────────────────
class AdmissionEnquiry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    dob: str
    applying_class: str
    parent_name: str
    phone: str
    email: Optional[str] = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


class AdmissionEnquiryCreate(SQLModel):
    student_name: str
    dob: str
    applying_class: str
    parent_name: str
    phone: str
    email: Optional[str] = None


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    # category: "events" | "trips" | "sports" | "academic"
    category: str
    image_url: Optional[str] = None
    date: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EventCreate(SQLModel):
    title: str
    description: Optional[str] = None
    category: str
    image_url: Optional[str] = None
    date: Optional[str] = None


# ── Faculty Table ──────────────────────────────────────────────────────────────
class Faculty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str                           # e.g. "Mathematics Teacher"
    qualification: Optional[str] = None  # e.g. "M.Sc. (Math), B.Ed."
    bio: Optional[str] = None
    icon: str = Field(default="fas fa-chalkboard-teacher")  # FontAwesome class
    avatar_class: Optional[str] = None  # extra CSS class e.g. "fa-admin"
    is_leader: bool = Field(default=False)  # True for Admin / Head Mistress
    sort_order: int = Field(default=99)     # lower = appears first
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FacultyCreate(SQLModel):
    name: str
    role: str
    qualification: Optional[str] = None
    bio: Optional[str] = None
    icon: str = "fas fa-chalkboard-teacher"
    avatar_class: Optional[str] = None
    is_leader: bool = False
    sort_order: int = 99


class FacultyUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None
    qualification: Optional[str] = None
    bio: Optional[str] = None
    icon: Optional[str] = None
    avatar_class: Optional[str] = None
    is_leader: Optional[bool] = None
    sort_order: Optional[int] = None


# ── Seed Data ─────────────────────────────────────────────────────────────────
DEFAULT_FACULTY = [
    FacultyCreate(
        name="Mr. Raghavendra Ashrit",
        role="Administrator",
        qualification="Founder & Administrator",
        bio="Founder & Administrator of K.B.D. Educational Trust (Regd.) | Visionary leader since Est. 1998.",
        icon="fas fa-user-shield",
        avatar_class="fa-admin",
        is_leader=True,
        sort_order=1,
    ),
    FacultyCreate(
        name="Mrs. Veena Ashrit",
        role="Head Mistress",
        qualification="Head Mistress",
        bio="Head Mistress of K.B.D. English Medium Primary & High School | Dedicated to academic excellence.",
        icon="fas fa-user-graduate",
        avatar_class="fa-hm",
        is_leader=True,
        sort_order=2,
    ),
    FacultyCreate(
        name="Mr. Raju Naik",
        role="Mathematics Teacher",
        qualification="M.Sc. (Math), B.Ed.",
        bio="Expert in competitive exam preparation.",
        icon="fas fa-chalkboard-teacher",
        sort_order=3,
    ),
    FacultyCreate(
        name="Mrs. Lakshmi Devi",
        role="English Teacher",
        qualification="M.A. (English), B.Ed.",
        bio="Passionate about language and literature.",
        icon="fas fa-user-graduate",
        sort_order=4,
    ),
    FacultyCreate(
        name="Mr. Siddappa",
        role="Social Science Teacher",
        qualification="M.A. (History), B.Ed.",
        bio="Brings history to life in the classroom.",
        icon="fas fa-user-tie",
        sort_order=5,
    ),
    FacultyCreate(
        name="Mrs. Rajeshwari",
        role="Kannada Teacher",
        qualification="M.A. (Kannada), B.Ed.",
        bio="Dedicated to language preservation and learning.",
        icon="fas fa-chalkboard-teacher",
        sort_order=6,
    ),
]


def seed_faculty(session: Session):
    """Insert default faculty only if table is empty."""
    existing = session.exec(select(Faculty)).first()
    if existing:
        return
    for f in DEFAULT_FACULTY:
        session.add(Faculty(**f.dict()))
    session.commit()


# ── Lifespan (startup hook) ────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_faculty(session)
    yield


# ── FastAPI App ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="KBD School API",
    version="1.0.0",
    description="Backend API for K.B.D. English Medium School website",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ───────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "KBD School API"}


# ── Admission Enquiry Routes ───────────────────────────────────────────────────
@app.post("/api/admissions", status_code=201, tags=["Admissions"])
def create_enquiry(enquiry: AdmissionEnquiryCreate):
    """Save an admission enquiry to the database."""
    with Session(engine) as session:
        db_enquiry = AdmissionEnquiry(**enquiry.dict())
        session.add(db_enquiry)
        session.commit()
        session.refresh(db_enquiry)
        return db_enquiry


@app.get("/api/admissions", tags=["Admissions"])
def list_enquiries():
    """List all admission enquiries (admin use)."""
    with Session(engine) as session:
        enquiries = session.exec(select(AdmissionEnquiry)).all()
        return {"total": len(enquiries), "data": enquiries}


@app.delete("/api/admissions/{enquiry_id}", tags=["Admissions"])
def delete_enquiry(enquiry_id: int):
    """Delete an admission enquiry."""
    with Session(engine) as session:
        db = session.get(AdmissionEnquiry, enquiry_id)
        if not db:
            raise HTTPException(status_code=404, detail="Enquiry not found")
        session.delete(db)
        session.commit()
        return {"ok": True, "message": f"Enquiry #{enquiry_id} deleted"}


# ── Events / Gallery Routes ────────────────────────────────────────────────────
@app.get("/api/events", tags=["Events"])
def list_events():
    """List all events / gallery items."""
    with Session(engine) as session:
        events = session.exec(select(Event)).all()
        return {"total": len(events), "data": events}


@app.post("/api/events", status_code=201, tags=["Events"])
def create_event(event: EventCreate):
    """Create a new event / gallery item."""
    with Session(engine) as session:
        db_event = Event(**event.dict())
        session.add(db_event)
        session.commit()
        session.refresh(db_event)
        return db_event


@app.put("/api/events/{event_id}", tags=["Events"])
def update_event(event_id: int, event: EventCreate):
    """Update an existing event."""
    with Session(engine) as session:
        db_event = session.get(Event, event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")
        event_data = event.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(db_event, key, value)
        session.add(db_event)
        session.commit()
        session.refresh(db_event)
        return db_event


@app.delete("/api/events/{event_id}", tags=["Events"])
def delete_event(event_id: int):
    """Delete an event."""
    with Session(engine) as session:
        db_event = session.get(Event, event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")
        session.delete(db_event)
        session.commit()
        return {"ok": True, "message": f"Event #{event_id} deleted"}


# ── Faculty Routes ─────────────────────────────────────────────────────────────
@app.get("/api/faculty", tags=["Faculty"])
def list_faculty():
    """List all faculty members sorted by sort_order."""
    with Session(engine) as session:
        faculty = session.exec(
            select(Faculty).order_by(Faculty.sort_order, Faculty.id)
        ).all()
        return {"total": len(faculty), "data": faculty}


@app.get("/api/faculty/{faculty_id}", tags=["Faculty"])
def get_faculty(faculty_id: int):
    """Get a single faculty member by ID."""
    with Session(engine) as session:
        f = session.get(Faculty, faculty_id)
        if not f:
            raise HTTPException(status_code=404, detail="Faculty not found")
        return f


@app.post("/api/faculty", status_code=201, tags=["Faculty"])
def create_faculty(faculty: FacultyCreate):
    """Add a new faculty member."""
    with Session(engine) as session:
        db_f = Faculty(**faculty.dict())
        session.add(db_f)
        session.commit()
        session.refresh(db_f)
        return db_f


@app.put("/api/faculty/{faculty_id}", tags=["Faculty"])
def update_faculty(faculty_id: int, faculty: FacultyUpdate):
    """Update an existing faculty member (partial update supported)."""
    with Session(engine) as session:
        db_f = session.get(Faculty, faculty_id)
        if not db_f:
            raise HTTPException(status_code=404, detail="Faculty not found")
        update_data = faculty.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_f, key, value)
        session.add(db_f)
        session.commit()
        session.refresh(db_f)
        return db_f


@app.delete("/api/faculty/{faculty_id}", tags=["Faculty"])
def delete_faculty(faculty_id: int):
    """Delete a faculty member."""
    with Session(engine) as session:
        db_f = session.get(Faculty, faculty_id)
        if not db_f:
            raise HTTPException(status_code=404, detail="Faculty not found")
        session.delete(db_f)
        session.commit()
        return {"ok": True, "message": f"Faculty #{faculty_id} deleted"}

