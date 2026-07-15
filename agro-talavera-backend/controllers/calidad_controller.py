from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import schemas, metricas_calidad, padron_cultivo
from config import get_db

router = APIRouter(prefix="/api", tags=["calidad"])

# Parámetros de negocio (Simulados para la lógica Comparar_parametros)
MIN_ALMIDON = 15.0
MAX_ALMIDON = 25.0

@router.post("/caracteristicas")
def registrar_caracteristicas(carac: schemas.CaracteristicaCreate, db: Session = Depends(get_db)):
    # Aquí podríamos guardar las características en una tabla, por ahora solo confirmamos recepción
    return {"message": "Características registradas correctamente", "lote_id": carac.lote_id}

@router.post("/atributos")
def registrar_atributos():
    # Similar al anterior, para guardar atributos del entorno o de los equipos
    return {"message": "Atributos vinculados"}

@router.post("/evaluacion", response_model=schemas.EvaluacionResponse)
def registro_evaluacion(evaluacion: schemas.EvaluacionCreate, db: Session = Depends(get_db)):
    # Verificar si el lote existe
    lote = db.query(padron_cultivo.PadronCultivo).filter(padron_cultivo.PadronCultivo.id == evaluacion.lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    # Lógica de Negocio: Comparar_parametros()
    estado = "DESAPROBADO"
    if MIN_ALMIDON <= evaluacion.porcentaje_almidon <= MAX_ALMIDON:
        estado = "APROBADO"

    nueva_metrica = metricas_calidad.MetricasCalidad(
        lote_id=evaluacion.lote_id,
        peso_muestra=evaluacion.peso_muestra,
        porcentaje_almidon=evaluacion.porcentaje_almidon,
        estado=estado
    )
    db.add(nueva_metrica)
    db.commit()
    db.refresh(nueva_metrica)

    return nueva_metrica
