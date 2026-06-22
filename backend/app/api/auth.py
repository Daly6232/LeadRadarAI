from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register():
    return {"status":"register endpoint"}

@router.post("/login")
def login():
    return {"status":"login endpoint"}
