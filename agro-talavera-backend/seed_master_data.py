import sqlite3
import os

db_path = "database.db"

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
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for tipo in tipos_papa:
        # Check if already exists for this tipo
        cursor.execute("SELECT COUNT(*) FROM eventos_calidad WHERE tipo_producto = ? AND producto_id IS NULL", (tipo,))
        count = cursor.fetchone()[0]

        if count == 0:
            for p in parametros_base:
                # Insert into eventos_calidad (Master Data row)
                cursor.execute("""
                    INSERT INTO eventos_calidad 
                    (producto_id, cod_atributo, descripcion, unidad_medida, estandar, nivel_calidad_p, min, max, tipo_producto)
                    VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (p["cod_atributo"], p["descripcion"], p["unidad_medida"], p["estandar"], p["nivel_calidad_p"], p["min"], p["max"], tipo))
                
                evento_id = cursor.lastrowid
                
                # Insert into parametros_calidad
                cursor.execute("""
                    INSERT INTO parametros_calidad
                    (evento_id, cod_atributo, descripcion, nivel_calidad_p, min, max)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (evento_id, p["cod_atributo"], p["descripcion"], p["nivel_calidad_p"], p["min"], p["max"]))
            
            print(f"Master Data seeded for {tipo}.")
        else:
            print(f"Master Data already exists for {tipo}.")

    conn.commit()
    conn.close()
    print("Master Data seeding process completed!")

if __name__ == "__main__":
    seed_db()
