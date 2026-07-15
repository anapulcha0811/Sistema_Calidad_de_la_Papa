from fastapi import APIRouter, HTTPException
from models.schemas import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(request: LoginRequest):
    # Dummy authentication for demonstration
    if request.usuario == "teriyaki" and request.password == "admin123":
        return {"message": "Login exitoso", "status": "ok"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
