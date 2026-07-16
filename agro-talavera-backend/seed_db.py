import sys
import os
import random
from datetime import datetime, timedelta

# Add backend dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SessionLocal, engine, Base
from models import padron_cultivo, producto_agricola, eventos_calidad, parametros_calidad, metricas_calidad, informe_calidad, estadisticos_calidad

# Import seed_master_data logic
from seed_master_data import seed_db as seed_master_data_func

def seed_data():
    # 1. Drop and recreate all tables
    print("Recreando base de datos...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 2. Re-seed Master Data (Admin Parameters)
    print("Pre-cargando Parámetros Maestros del Administrador...")
    seed_master_data_func()

    db = SessionLocal()

    try:
        tipos_cultivo = ["Papa Blanca", "Papa Amarilla", "Papa Canchán", "Papa Yungay", "Papa Huayro", "Papa Perricholi", "Papa Tumbay"]
        nombres_lote = ["Fundo El Sol", "Hacienda San José", "Valle Verde", "Pampa Alta", "Santa Rosa", "Los Sauces", "Mirador"]

        print("Generando EXACTAMENTE 4 Lotes de Padrón...")
        lotes_creados = []
        for i in range(1, 5):
            fecha = datetime.now() - timedelta(days=random.randint(1, 30))
            tipo = random.choice(tipos_cultivo)
            lote = padron_cultivo.PadronCultivo(
                codigo=f"LOT-2026-{i:03d}",
                nombre=f"{random.choice(nombres_lote)} - Sector {random.randint(1,9)}",
                cantidad_lote=round(random.uniform(1000, 15000), 2),
                fecha_ingreso=fecha.date(),
                tipo_producto=tipo,
                cod_inspeccion=f"INS-{fecha.strftime('%Y%m%d')}-{i:03d}"
            )
            db.add(lote)
            lotes_creados.append(lote)
        
        db.commit()

        print("Generando Productos, Eventos y Evaluaciones para los 4 lotes...")
        for lote in lotes_creados:
            # CU2: Cada lote tiene 1 producto principal a evaluar (Visual)
            cuali = random.choice(["Óptimo", "Aceptable"])
            prod = producto_agricola.ProductoAgricola(
                padron_id=lote.id,
                codigo=lote.codigo,
                cod_atributo=f"ATR-VIS-{random.randint(100,999)}",
                descripcion=f"Inspección Visual de {lote.tipo_producto}",
                cualitativo=cuali,
                unidad_medida="Visual"
            )
            db.add(prod)
            db.commit()
            db.refresh(prod)

            # CU3: Obtener parámetros globales del administrador para este tipo de papa
            parametros_globales = db.query(eventos_calidad.EventosCalidad).filter(
                eventos_calidad.EventosCalidad.tipo_producto == lote.tipo_producto,
                eventos_calidad.EventosCalidad.producto_id == None
            ).all()

            metricas_creadas = []
            total_aprobados = 0
            
            for param_admin in parametros_globales:
                margen = (param_admin.max - param_admin.min) * 0.4
                # Simular resultado de laboratorio
                if random.random() < 0.7:
                    resultado = round(random.uniform(param_admin.min, param_admin.max), 2)
                else:
                    resultado = round(random.uniform(param_admin.min - margen, param_admin.max + margen), 2)
                
                estado = "APROBADO" if param_admin.min <= resultado <= param_admin.max else "DESAPROBADO"
                if estado == "APROBADO": total_aprobados += 1
                
                metrica = metricas_calidad.MetricasCalidad(
                    lote_id=lote.id,
                    evento_id=param_admin.id,
                    cod_inspeccion=lote.cod_inspeccion,
                    cod_muestra=f"MUE-{lote.id}-{param_admin.id}-{random.randint(100,999)}",
                    fecha_control=(lote.fecha_ingreso + timedelta(days=1)).strftime("%Y-%m-%d"),
                    cod_atributo=param_admin.cod_atributo,
                    descripcion=param_admin.descripcion,
                    resultado=resultado,
                    simbolo="=" if estado == "APROBADO" else ("<" if resultado < param_admin.min else ">"),
                    nivel_calidad_m=param_admin.nivel_calidad_p,
                    tamano_muestra=1.0,
                    estado=estado
                )
                db.add(metrica)
                metricas_creadas.append(metrica)
            
            db.commit()

            # Consolidar Informes (CU4) - Lógica de 100% de aprobación
            estado_gral = "APROBADO" if total_aprobados == len(parametros_globales) else "DESAPROBADO"
            informe = informe_calidad.InformeCalidad(
                lote_id=lote.id,
                cod_inspeccion=lote.cod_inspeccion,
                aprobado=estado_gral,
                nivel_calidad_m="ALTA" if estado_gral == "APROBADO" else "BAJA",
                tamano_muestra=len(parametros_globales)
            )
            db.add(informe)
            db.commit()
            db.refresh(informe)

            for m in metricas_creadas:
                db.refresh(m)
                estat = estadisticos_calidad.EstadisticosCalidad(
                    informe_id=informe.id,
                    cod_atributo=m.cod_atributo,
                    descripcion=m.descripcion,
                    nivel_calidad_m=m.nivel_calidad_m
                )
                db.add(estat)
            db.commit()

        print("¡Base de datos poblada con éxito con solo 4 lotes de prueba coherentes!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
