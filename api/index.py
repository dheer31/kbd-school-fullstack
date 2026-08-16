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


# ── NewsItem Table ────────────────────────────────────────────────────────────
class NewsItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tag: str = Field(default="News")          # e.g. "Featured", "New", "Upcoming", "Notice"
    title: str
    description: Optional[str] = None
    date: Optional[str] = None                # e.g. "August 15, 2025"
    link: Optional[str] = Field(default="#")  # href for the card button
    link_text: Optional[str] = Field(default="Read More")  # button label
    is_featured: bool = Field(default=False)  # featured card gets dark background
    sort_order: int = Field(default=99)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NewsItemCreate(SQLModel):
    tag: str = "News"
    title: str
    description: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = "#"
    link_text: Optional[str] = "Read More"
    is_featured: bool = False
    sort_order: int = 99


class NewsItemUpdate(SQLModel):
    tag: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    link: Optional[str] = None
    link_text: Optional[str] = None
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None


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
DEFAULT_NEWS = [
    NewsItemCreate(
        tag="Featured",
        title="Independence Day Celebration 2025",
        description="K.B.D. School celebrated India's 79th Independence Day with great patriotic fervor. Students performed cultural programs, flag hoisting, and march-past.",
        date="August 15, 2025",
        link="#",
        link_text="Read More",
        is_featured=True,
        sort_order=1,
    ),
    NewsItemCreate(
        tag="New",
        title="Admission Open for 2025-26",
        description="Applications for the academic year 2025-26 are now open for all classes from 1 to 10. Limited seats available. Apply early!",
        date="July 28, 2025",
        link="#admissions",
        link_text="Apply Now",
        is_featured=False,
        sort_order=2,
    ),
    NewsItemCreate(
        tag="Upcoming",
        title="Annual Sports Day 2025",
        description="The Annual Sports Day will be held on September 20th. All students are encouraged to participate in various sporting events and competitions.",
        date="September 20, 2025",
        link="#",
        link_text="Learn More",
        is_featured=False,
        sort_order=3,
    ),
    NewsItemCreate(
        tag="Notice",
        title="Parent-Teacher Meeting",
        description="The quarterly Parent-Teacher Meeting is scheduled for August 25, 2025. All parents are requested to attend to discuss their child's progress.",
        date="August 25, 2025",
        link="#",
        link_text="Details",
        is_featured=False,
        sort_order=4,
    ),
]


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


def seed_news(session: Session):
    """Insert default news items only if table is empty."""
    existing = session.exec(select(NewsItem)).first()
    if existing:
        return
    for n in DEFAULT_NEWS:
        session.add(NewsItem(**n.dict()))
    session.commit()


# ── Lifespan (startup hook) ────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_faculty(session)
        seed_news(session)
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


# ── News Routes ────────────────────────────────────────────────────────────────
@app.get("/api/news", tags=["News"])
def list_news():
    """List all news items sorted by sort_order."""
    with Session(engine) as session:
        items = session.exec(
            select(NewsItem).order_by(NewsItem.sort_order, NewsItem.id)
        ).all()
        return {"total": len(items), "data": items}


@app.get("/api/news/{news_id}", tags=["News"])
def get_news(news_id: int):
    """Get a single news item by ID."""
    with Session(engine) as session:
        item = session.get(NewsItem, news_id)
        if not item:
            raise HTTPException(status_code=404, detail="News item not found")
        return item


@app.post("/api/news", status_code=201, tags=["News"])
def create_news(news: NewsItemCreate):
    """Create a new news/announcement item."""
    with Session(engine) as session:
        db_item = NewsItem(**news.dict())
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item


@app.put("/api/news/{news_id}", tags=["News"])
def update_news(news_id: int, news: NewsItemUpdate):
    """Update an existing news item (partial update supported)."""
    with Session(engine) as session:
        db_item = session.get(NewsItem, news_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="News item not found")
        update_data = news.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item


@app.delete("/api/news/{news_id}", tags=["News"])
def delete_news(news_id: int):
    """Delete a news item."""
    with Session(engine) as session:
        db_item = session.get(NewsItem, news_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="News item not found")
        session.delete(db_item)
        session.commit()
        return {"ok": True, "message": f"News item #{news_id} deleted"}
