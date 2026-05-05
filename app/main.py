from fastapi import FastAPI
from app.routers import users, notes
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}