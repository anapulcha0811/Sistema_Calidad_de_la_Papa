from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import schemas, metricas_calidad, padron_cultivo, producto_agricola, eventos_calidad, parametros_calidad, informe_calidad, estadisticos_calidad
from config import get_db

router = APIRouter(prefix="/api", tags=["calidad"])
@router.post("/caracteristicas")
def registrar_caracteristicas(carac: schemas.CaracteristicaCreate, db: Session = Depends(get_db)):
    nuevo_producto = producto_agricola.ProductoAgricola(
        padron_id=carac.lote_id,
        codigo=carac.codigo,
        cod_atributo=carac.cod_atributo,
        descripcion=carac.descripcion,
        cualitativo=carac.cualitativo,
        unidad_medida=carac.unidad_medida
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return {"message": "Características registradas correctamente", "lote_id": carac.lote_id}

@router.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(producto_agricola.ProductoAgricola).all()
    result = []
    for p in productos:
        lote = db.query(padron_cultivo.PadronCultivo).filter(padron_cultivo.PadronCultivo.id == p.padron_id).first()
        if lote:
            result.append({
                "id": p.id,
                "padron_id": p.padron_id,
                "codigo": p.codigo,
                "cod_atributo": p.cod_atributo,
                "descripcion": p.descripcion,
                "cualitativo": p.cualitativo,
                "unidad_medida": p.unidad_medida,
                "tipo_producto": lote.tipo_producto,
                "nombre_lote": lote.nombre,
                "cod_inspeccion": lote.cod_inspeccion
            })
    return result

@router.get("/productos/lote/{lote_id}")
def listar_productos_por_lote(lote_id: int, db: Session = Depends(get_db)):
    return db.query(producto_agricola.ProductoAgricola).filter(producto_agricola.ProductoAgricola.padron_id == lote_id).all()

@router.get("/eventos/producto/{producto_id}")
def listar_eventos_por_producto(producto_id: int, db: Session = Depends(get_db)):
    return db.query(eventos_calidad.EventosCalidad).filter(eventos_calidad.EventosCalidad.producto_id == producto_id).all()

@router.post("/eventos")
def registrar_eventos(evento: schemas.EventoCalidadCreate, db: Session = Depends(get_db)):
    nuevo_evento = eventos_calidad.EventosCalidad(
        producto_id=evento.producto_id,
        cod_atributo=evento.cod_atributo,
        descripcion=evento.descripcion,
        unidad_medida=evento.unidad_medida,
        estandar=evento.estandar,
        nivel_calidad_p=evento.nivel_calidad_p,
        min=evento.min,
        max=evento.max,
        tipo_producto=evento.tipo_producto
    )
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)

    # Autocompletado: Insertar simultáneamente en Parametros_Calidad según el diagrama BD
    nuevo_parametro = parametros_calidad.ParametrosCalidad(
        evento_id=nuevo_evento.id,
        cod_atributo=evento.cod_atributo,
        descripcion=evento.descripcion,
        nivel_calidad_p=evento.nivel_calidad_p,
        min=evento.min,
        max=evento.max
    )
    db.add(nuevo_parametro)
    db.commit()

    return {"message": "Eventos y Parámetros de calidad guardados correctamente", "evento_id": nuevo_evento.id}

@router.get("/configuracion/parametros")
def obtener_todos_parametros_globales(db: Session = Depends(get_db)):
    return db.query(eventos_calidad.EventosCalidad).filter(
        eventos_calidad.EventosCalidad.producto_id == None
    ).all()

@router.get("/configuracion/parametros/{tipo_producto}")
def obtener_parametros_globales(tipo_producto: str, db: Session = Depends(get_db)):
    return db.query(eventos_calidad.EventosCalidad).filter(
        eventos_calidad.EventosCalidad.tipo_producto == tipo_producto,
        eventos_calidad.EventosCalidad.producto_id == None
    ).all()

@router.post("/configuracion/parametros")
def guardar_parametro_global(param: schemas.ParametroGlobalCreate, db: Session = Depends(get_db)):
    nuevo_evento = eventos_calidad.EventosCalidad(
        producto_id=None, # Indicador de que es Master Data
        cod_atributo=param.cod_atributo,
        descripcion=param.descripcion,
        unidad_medida=param.unidad_medida,
        estandar=param.estandar,
        nivel_calidad_p=param.nivel_calidad_p,
        min=param.min,
        max=param.max,
        tipo_producto=param.tipo_producto
    )
    db.add(nuevo_evento)
    db.commit()
    
    nuevo_parametro = parametros_calidad.ParametrosCalidad(
        evento_id=nuevo_evento.id,
        cod_atributo=param.cod_atributo,
        descripcion=param.descripcion,
        nivel_calidad_p=param.nivel_calidad_p,
        min=param.min,
        max=param.max
    )
    db.add(nuevo_parametro)
    db.commit()
    
    return {"message": "Parámetro maestro guardado"}

@router.put("/configuracion/parametros/{evento_id}")
def actualizar_parametro_global(evento_id: int, param: schemas.ParametroGlobalCreate, db: Session = Depends(get_db)):
    evento = db.query(eventos_calidad.EventosCalidad).filter(eventos_calidad.EventosCalidad.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
        
    evento.cod_atributo = param.cod_atributo
    evento.descripcion = param.descripcion
    evento.unidad_medida = param.unidad_medida
    evento.estandar = param.estandar
    evento.nivel_calidad_p = param.nivel_calidad_p
    evento.min = param.min
    evento.max = param.max
    evento.tipo_producto = param.tipo_producto
    
    parametro = db.query(parametros_calidad.ParametrosCalidad).filter(parametros_calidad.ParametrosCalidad.evento_id == evento_id).first()
    if parametro:
        parametro.cod_atributo = param.cod_atributo
        parametro.descripcion = param.descripcion
        parametro.nivel_calidad_p = param.nivel_calidad_p
        parametro.min = param.min
        parametro.max = param.max
        
    db.commit()
    return {"message": "Parámetro maestro actualizado"}

@router.post("/atributos")
def registrar_atributos():
    return {"message": "Atributos vinculados"}

@router.get("/eventos_lista")
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(eventos_calidad.EventosCalidad).all()

import random
from typing import List

@router.post("/evaluacion", response_model=List[schemas.EvaluacionResponse])
def registro_evaluacion(req: schemas.EvaluacionManualRequest, db: Session = Depends(get_db)):
    lote = db.query(padron_cultivo.PadronCultivo).filter(padron_cultivo.PadronCultivo.id == req.lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
        
    if not req.resultados:
        raise HTTPException(status_code=400, detail="Debe ingresar resultados de laboratorio.")
        
    metricas_creadas = []
    total_aprobados = 0
    total_muestras = len(req.resultados)
    
    for item in req.resultados:
        evento_id = int(item.get("evento_id"))
        resultado_ingresado = float(item.get("valor", 0))
        
        evento = db.query(eventos_calidad.EventosCalidad).filter(eventos_calidad.EventosCalidad.id == evento_id).first()
        if not evento:
            continue
            
        estado = "DESAPROBADO"
        if evento.min <= resultado_ingresado <= evento.max:
            estado = "APROBADO"
            total_aprobados += 1
            
        cod_muestra = f"MUE-{req.lote_id}-{evento.id}-{random.randint(100,999)}"
            
        nueva_metrica = metricas_calidad.MetricasCalidad(
            lote_id=req.lote_id,
            evento_id=evento.id,
            cod_inspeccion=req.cod_inspeccion,
            cod_muestra=cod_muestra,
            fecha_control=req.fecha_control,
            cod_atributo=evento.cod_atributo,
            descripcion=evento.descripcion,
            resultado=resultado_ingresado,
            simbolo="=" if estado == "APROBADO" else ("<" if resultado_ingresado < evento.min else ">"),
            nivel_calidad_m=evento.nivel_calidad_p,
            tamano_muestra=1.0,
            estado=estado
        )
        db.add(nueva_metrica)
        metricas_creadas.append(nueva_metrica)
        
    db.commit()

    # Consolidar en Informe_Calidad
    estado_general = "APROBADO" if total_aprobados == total_muestras else "DESAPROBADO"
    nuevo_informe = informe_calidad.InformeCalidad(
        lote_id=req.lote_id,
        cod_inspeccion=req.cod_inspeccion,
        aprobado=estado_general,
        nivel_calidad_m="ALTA" if estado_general == "APROBADO" else "BAJA",
        tamano_muestra=total_muestras
    )
    db.add(nuevo_informe)
    db.commit()
    db.refresh(nuevo_informe)

    # Consolidar en Estadisticos_Calidad
    for m in metricas_creadas:
        db.refresh(m)
        nuevo_estat = estadisticos_calidad.EstadisticosCalidad(
            informe_id=nuevo_informe.id,
            cod_atributo=m.cod_atributo,
            descripcion=m.descripcion,
            nivel_calidad_m=m.nivel_calidad_m
        )
        db.add(nuevo_estat)
        
    db.commit()

    return metricas_creadas

@router.get("/evaluacion/lote/{lote_id}")
def obtener_evaluacion_lote(lote_id: int, db: Session = Depends(get_db)):
    metricas = db.query(metricas_calidad.MetricasCalidad).filter(metricas_calidad.MetricasCalidad.lote_id == lote_id).all()
    informe = db.query(informe_calidad.InformeCalidad).filter(informe_calidad.InformeCalidad.lote_id == lote_id).order_by(informe_calidad.InformeCalidad.id.desc()).first()
    
    if not informe:
        raise HTTPException(status_code=404, detail="No hay evaluación para este lote")
        
    metricas_data = []
    for m in metricas:
        evento = db.query(eventos_calidad.EventosCalidad).filter(eventos_calidad.EventosCalidad.id == m.evento_id).first()
        metricas_data.append({
            "cod_atributo": m.cod_atributo,
            "descripcion": m.descripcion,
            "resultado": m.resultado,
            "estado": m.estado,
            "min": evento.min if evento else 0,
            "max": evento.max if evento else 0,
            "unidad": evento.unidad_medida if evento else ""
        })
        
    return {
        "lote_id": lote_id,
        "cod_inspeccion": informe.cod_inspeccion,
        "tamano_muestra": informe.tamano_muestra,
        "estado_general": informe.aprobado,
        "metricas": metricas_data
    }
