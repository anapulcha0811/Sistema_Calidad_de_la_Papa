import os
import sys

# Add backend dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SessionLocal
from models.eventos_calidad import EventosCalidad
from models.parametros_calidad import ParametrosCalidad

# Parameters
parametros_base = [
    {
        "cod_atributo": "ATR-HUM-01",
        "descripcion": "Humedad",
        "unidad_medida": "%",
        "estandar": "NTP 011.119 - Máx 14%",
        "nivel_calidad_p": "Alta",
        "min": 10.0,
        "max": 14.0
    },
    {
        "cod_atributo": "ATR-CAL-02",
        "descripcion": "Calibre (Tamaño)",
        "unidad_medida": "mm",
        "estandar": "NTP 011.119 - Calibre Comercial",
        "nivel_calidad_p": "Media",
        "min": 40.0,
        "max": 80.0
    },
    {
        "cod_atributo": "ATR-DAN-03",
        "descripcion": "Daños Mecánicos",
        "unidad_medida": "%",
        "estandar": "NTP 011.119 - Máx 5%",
        "nivel_calidad_p": "Alta",
        "min": 0.0,
        "max": 5.0
    }
]

tipos_papa = ["Papa Blanca", "Papa Amarilla", "Papa Canchán", "Papa Yungay", "Papa Huayro", "Papa Perricholi", "Papa Tumbay"]

def seed_db():
    db = SessionLocal()
    try:
        for tipo in tipos_papa:
            # Check if already exists for this tipo
            count = db.query(EventosCalidad).filter(EventosCalidad.tipo_producto == tipo, EventosCalidad.producto_id == None).count()

            if count == 0:
                for p in parametros_base:
                    evento = EventosCalidad(
                        producto_id=None,
                        cod_atributo=p["cod_atributo"],
                        descripcion=p["descripcion"],
                        unidad_medida=p["unidad_medida"],
                        estandar=p["estandar"],
                        nivel_calidad_p=p["nivel_calidad_p"],
                        min=p["min"],
                        max=p["max"],
                        tipo_producto=tipo
                    )
                    db.add(evento)
                    db.flush() # To get the id
                    
                    param = ParametrosCalidad(
                        evento_id=evento.id,
                        cod_atributo=p["cod_atributo"],
                        descripcion=p["descripcion"],
                        nivel_calidad_p=p["nivel_calidad_p"],
                        min=p["min"],
                        max=p["max"]
                    )
                    db.add(param)
                
                db.commit()
                print(f"Master Data seeded for {tipo}.")
            else:
                print(f"Master Data already exists for {tipo}.")

        print("Master Data seeding process completed!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
