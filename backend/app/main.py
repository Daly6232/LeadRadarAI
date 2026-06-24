from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models.user import Base as UserBase
from app.models.lead import Lead  # noqa

# Routers
from app.api.auth import router as auth_router
from app.api.leads import router as leads_router
from app.api.ai import router as ai_router
from app.routes.osm_scan import router as osm_router
from app.routes.dashboard import router as dashboard_router

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
UserBase.metadata.drop_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(leads_router)
app.include_router(ai_router)
app.include_router(osm_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "LeadRadar AI Backend Running", "version": "2.0.0"}
