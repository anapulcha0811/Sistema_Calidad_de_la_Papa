from fastapi import APIRouter, HTTPException
from models.schemas import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(request: LoginRequest):
    # Autenticación con Roles
    if request.usuario == "admin" and request.password == "admin123":
        return {"message": "Login exitoso", "status": "ok", "rol": "administrador"}
    elif request.usuario == "operador" and request.password == "operador123":
        return {"message": "Login exitoso", "status": "ok", "rol": "operador"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
