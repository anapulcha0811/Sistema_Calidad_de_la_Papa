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

@router.get("/historial")
def historial_evaluaciones(db: Session = Depends(get_db)):
    # Retorna todas las evaluaciones consolidadas por lote
    informes = db.query(informe_calidad.InformeCalidad).order_by(informe_calidad.InformeCalidad.id.desc()).all()
    historial = []
    for info in informes:
        lote = db.query(padron_cultivo.PadronCultivo).filter(padron_cultivo.PadronCultivo.id == info.lote_id).first()
        if lote:
            historial.append({
                "lote_codigo": lote.codigo,
                "lote_nombre": lote.nombre,
                "tipo_producto": lote.tipo_producto,
                "cod_inspeccion": info.cod_inspeccion,
                "tamano_muestra": info.tamano_muestra,
                "estado_general": info.aprobado,
                "nivel_calidad": info.nivel_calidad_m,
                "fecha": lote.fecha_ingreso # aproximación de fecha de evaluación
            })
    return historial

@router.get("/dashboard")
def dashboard_data(db: Session = Depends(get_db)):
    lotes_totales = db.query(padron_cultivo.PadronCultivo).count()
    
    # Actividad reciente: últimos 5 lotes o evaluaciones
    # Como simplificación, juntamos lotes y sus estados
    lotes = db.query(padron_cultivo.PadronCultivo).order_by(padron_cultivo.PadronCultivo.id.desc()).limit(5).all()
    
    actividad = []
    aprobados_total = 0
    evaluados_total = 0
    
    for lote in lotes:
        evaluacion = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.lote_id == lote.id).first()
        aprobado = False
        if evaluacion:
            evaluados_total += 1
            if evaluacion.estado == "APROBADO":
                aprobados_total += 1
                aprobado = True
                
        actividad.append({
            "codigo": lote.codigo,
            "fecha": lote.fecha_ingreso,
            "aprobado": aprobado
        })
        
    evaluaciones = db.query(metricas_calidad.MetricasCalidad).count()
    aprobados = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.estado == "APROBADO").count()
    desaprobados = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.estado == "DESAPROBADO").count()

    porcentaje = (aprobados / evaluaciones * 100) if evaluaciones > 0 else 0.0

    # Simular datos históricos para el gráfico de líneas (Últimos 7 días)
    fechas = ["D-6", "D-5", "D-4", "D-3", "D-2", "D-1", "Hoy"]
    import random
    tendencia_aprobacion = [random.randint(60, 95) for _ in range(7)]
    tendencia_evaluados = [random.randint(10, 50) for _ in range(7)]

    # Datos para Polar Area (Comparación de atributos globales)
    polar_labels = ["Humedad", "Almidón", "Calibre", "Peso", "Color"]
    polar_data = [random.randint(20, 100) for _ in range(5)]

    return {
        "lotes_totales": lotes_totales,
        "muestras_evaluadas": evaluaciones,
        "aprobados": aprobados,
        "desaprobados": desaprobados,
        "porcentaje_aprobacion": round(porcentaje, 1),
        "actividad_reciente": actividad,
        "tendencia": {
            "fechas": fechas,
            "aprobacion": tendencia_aprobacion,
            "volumen": tendencia_evaluados
        },
        "polar": {
            "labels": polar_labels,
            "data": polar_data
        }
    }

@router.get("/estadisticas/{lote_id}")
def reporte_estadistico_lote(lote_id: int, db: Session = Depends(get_db)):
    lote = db.query(padron_cultivo.PadronCultivo).filter(padron_cultivo.PadronCultivo.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
        
    metricas = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.lote_id == lote_id).all()
    
    if not metricas:
        raise HTTPException(status_code=400, detail="Este lote no tiene evaluaciones de calidad. Por favor vaya al CU4 primero.")
        
    total = len(metricas)
    aprobados = sum(1 for m in metricas if m.estado == "APROBADO")
    desaprobados = sum(1 for m in metricas if m.estado == "DESAPROBADO")
    
    # We can also group by atributo
    atributos_data = []
    for m in metricas:
        atributos_data.append({
            "cod_atributo": m.cod_atributo,
            "descripcion": m.descripcion,
            "resultado": m.resultado,
            "estado": m.estado
        })
    
    return {
        "lote_codigo": lote.codigo,
        "lote_nombre": lote.nombre,
        "fecha_control": metricas[0].fecha_control,
        "cod_inspeccion": metricas[0].cod_inspeccion,
        "total_muestras": total,
        "aprobados": aprobados,
        "desaprobados": desaprobados,
        "porcentaje_aprobacion": round((aprobados / total * 100), 2) if total > 0 else 0,
        "detalle": atributos_data
    }
