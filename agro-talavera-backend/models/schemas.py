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
    codigo: str
    cod_atributo: str
    descripcion: str
    cualitativo: str
    unidad_medida: str

class EventoCalidadCreate(BaseModel):
    producto_id: int
    cod_atributo: str
    descripcion: str
    unidad_medida: str
    estandar: str
    nivel_calidad_p: str
    min: float
    max: float
    tipo_producto: str

class EvaluacionGenerarRequest(BaseModel):
    lote_id: int
    cod_inspeccion: str
    fecha_control: str

class EvaluacionManualRequest(BaseModel):
    lote_id: int
    cod_inspeccion: str
    fecha_control: str
    resultados: list = [] # list of {"evento_id": int, "valor": float}

class ParametroGlobalCreate(BaseModel):
    tipo_producto: str
    cod_atributo: str
    descripcion: str
    unidad_medida: str
    estandar: str
    nivel_calidad_p: str
    min: float
    max: float

class EvaluacionResponse(BaseModel):
    id: int
    cod_muestra: str
    cod_atributo: str
    descripcion: str
    resultado: float
    estado: str

    class Config:
        from_attributes = True
