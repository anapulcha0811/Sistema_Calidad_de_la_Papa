from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import schemas, padron_cultivo
from config import get_db

router = APIRouter(prefix="/api/lotes", tags=["lotes"])

@router.post("", response_model=schemas.CultivoResponse)
def introducir_datos(lote: schemas.CultivoCreate, db: Session = Depends(get_db)):
    db_lote = padron_cultivo.PadronCultivo(**lote.model_dump())
    db.add(db_lote)
    try:
        db.commit()
        db.refresh(db_lote)
        return db_lote
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al guardar el lote. Verifica que el código no esté duplicado.")

@router.get("", response_model=list[schemas.CultivoResponse])
def obtener_lotes(db: Session = Depends(get_db)):
    return db.query(padron_cultivo.PadronCultivo).all()
