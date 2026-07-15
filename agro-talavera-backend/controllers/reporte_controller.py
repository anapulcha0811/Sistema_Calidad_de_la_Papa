from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import schemas, metricas_calidad, padron_cultivo, informe_calidad
from config import get_db

router = APIRouter(prefix="/api/reportes", tags=["reportes"])

@router.get("/estadisticos")
def reporte_estadistico(db: Session = Depends(get_db)):
    # Simulación de un reporte estadístico agrupando aprobados y desaprobados
    total = db.query(metricas_calidad.MetricasCalidad).count()
    aprobados = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.estado == "APROBADO").count()
    desaprobados = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.estado == "DESAPROBADO").count()
    
    return {
        "total_evaluaciones": total,
        "aprobados": aprobados,
        "desaprobados": desaprobados,
        "porcentaje_aprobacion": (aprobados / total * 100) if total > 0 else 0
    }

@router.get("/informe/{cod_inspeccion}")
def solicitar_datos_calidad(cod_inspeccion: str, db: Session = Depends(get_db)):
    lote = db.query(padron_cultivo.PadronCultivo).filter(padron_cultivo.PadronCultivo.cod_inspeccion == cod_inspeccion).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
        
    evaluacion = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.lote_id == lote.id).first()
    
    return {
        "lote_codigo": lote.codigo,
        "nombre": lote.nombre,
        "fecha": lote.fecha_ingreso,
        "evaluacion_realizada": True if evaluacion else False,
        "estado_final": evaluacion.estado if evaluacion else "PENDIENTE",
        "porcentaje_almidon": evaluacion.porcentaje_almidon if evaluacion else None
    }
