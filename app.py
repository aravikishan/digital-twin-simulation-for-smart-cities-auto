
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uvicorn
import json

# Database setup
DATABASE_URL = "sqlite:///./smart_city_simulation.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class SimulationData(Base):
    __tablename__ = "simulation_data"
    id = Column(Integer, primary_key=True, index=True)
    population = Column(Integer)
    traffic = Column(Integer)
    energy_usage = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    preferences = Column(String)

class SimulationSettings(Base):
    __tablename__ = "simulation_settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    traffic_model = Column(String)
    energy_model = Column(String)
    population_growth_rate = Column(Float)
    user = relationship("User")

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data(db_session):
    if not db_session.query(SimulationData).first():
        db_session.add(SimulationData(population=100000, traffic=5000, energy_usage=2500.5))
        db_session.commit()

# FastAPI app setup
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/simulation", response_class=HTMLResponse)
async def simulation_dashboard(request: Request):
    return templates.TemplateResponse("simulation.html", {"request": request})

@app.get("/api-docs", response_class=HTMLResponse)
async def api_docs(request: Request):
    return templates.TemplateResponse("api_docs.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def user_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# API Endpoints
@app.get("/api/simulation/data")
async def get_simulation_data(db: Session = Depends(get_db)):
    data = db.query(SimulationData).all()
    return data

@app.post("/api/simulation/start")
async def start_simulation():
    # Logic to start simulation
    return {"message": "Simulation started"}

@app.get("/api/simulation/settings")
async def get_simulation_settings(db: Session = Depends(get_db)):
    settings = db.query(SimulationSettings).all()
    return settings

@app.put("/api/simulation/settings")
async def update_simulation_settings(settings: SimulationSettings, db: Session = Depends(get_db)):
    db_settings = db.query(SimulationSettings).filter(SimulationSettings.id == settings.id).first()
    if db_settings is None:
        raise HTTPException(status_code=404, detail="Settings not found")
    db_settings.traffic_model = settings.traffic_model
    db_settings.energy_model = settings.energy_model
    db_settings.population_growth_rate = settings.population_growth_rate
    db.commit()
    db.refresh(db_settings)
    return db_settings

if __name__ == "__main__":
    # Seed demo data
    db = SessionLocal()
    seed_data(db)
    db.close()
    # Run the app
    uvicorn.run(app, host="0.0.0.0", port=8000)

