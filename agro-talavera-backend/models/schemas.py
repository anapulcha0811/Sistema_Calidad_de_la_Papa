from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class LoginRequest(BaseModel):
    usuario: str
    password: str

class CultivoCreate(BaseModel):
    codigo: str = Field(..., min_length=1)
    nombre: str = Field(..., min_length=1)
    cantidad_lote: float = Field(..., gt=0)
    fecha_ingreso: date
    tipo_producto: str = Field(..., min_length=1)
    cod_inspeccion: str = Field(..., min_length=1)

class CultivoResponse(CultivoCreate):
    id: int

    class Config:
        from_attributes = True

class CaracteristicaCreate(BaseModel):
    lote_id: int
    descripcion_muestra: str

class EvaluacionCreate(BaseModel):
    lote_id: int
    peso_muestra: float = Field(..., gt=0)
    porcentaje_almidon: float = Field(..., ge=0, le=100)

class EvaluacionResponse(BaseModel):
    id: int
    estado: str
    lote_id: int
    porcentaje_almidon: float

    class Config:
        from_attributes = True
