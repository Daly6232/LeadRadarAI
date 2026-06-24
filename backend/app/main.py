from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.leads import router as leads_router
from app.database import engine
from app.models.user import Base as UserBase
from app.models.lead import Lead  # noqa: F401 — must import to register with Base

app = FastAPI(title="LeadRadar AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    UserBase.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(leads_router)

@app.get("/")
def root():
    return {"message": "LeadRadar AI Backend Running", "version": "2.0.0"}
