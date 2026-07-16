import unittest
import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000/api"

class TestAgroTalaveraUseCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate a random code to avoid Unique Constraint errors on re-runs
        cls.random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        cls.lote_codigo = f"TEST-LT-{cls.random_suffix}"
        cls.lote_id = None
        cls.producto_id = None
        cls.evento_id = None

    def test_01_cu1_crear_lote(self):
        """Prueba del Caso de Uso 1: Registro en Padrón"""
        payload = {
            "codigo": self.lote_codigo,
            "nombre": "Producto de Prueba Unitaria",
            "cantidad_lote": 500,
            "fecha_ingreso": "2026-07-16",
            "tipo_producto": "Agricola",
            "cod_inspeccion": f"INS-{self.random_suffix}"
        }
        res = requests.post(f"{BASE_URL}/lotes", json=payload)
        self.assertEqual(res.status_code, 200, "El lote no se pudo crear")
        data = res.json()
        self.assertIn("id", data)
        self.__class__.lote_id = data["id"]
        print(f"\n[OK] CU1: Lote creado con ID {self.lote_id}")

    def test_02_cu2_registrar_caracteristica(self):
        """Prueba del Caso de Uso 2: Registrar Característica"""
        payload = {
            "lote_id": self.lote_id,
            "codigo": f"CAR-{self.random_suffix}",
            "cod_atributo": "ATR-HUM",
            "descripcion": "Humedad Relativa",
            "cualitativo": "No",
            "unidad_medida": "%"
        }
        res = requests.post(f"{BASE_URL}/caracteristicas", json=payload)
        self.assertEqual(res.status_code, 200, "No se pudo registrar la característica")
        print("[OK] CU2: Característica registrada")
        
        # We need the producto_id for the next test. We fetch all productos and find ours.
        res_prod = requests.get(f"{BASE_URL}/productos")
        productos = res_prod.json()
        for p in productos:
            if p["padron_id"] == self.lote_id:
                self.__class__.producto_id = p["id"]
                break
        self.assertIsNotNone(self.producto_id, "No se encontró el producto_id asociado al lote")

    def test_03_cu3_registrar_evento(self):
        """Prueba del Caso de Uso 3: Registrar Eventos de Calidad"""
        payload = {
            "producto_id": self.producto_id,
            "cod_atributo": "ATR-HUM",
            "descripcion": "Humedad",
            "unidad_medida": "%",
            "estandar": "NTP-ISO",
            "nivel_calidad_p": "Alta",
            "min": 10.0,
            "max": 20.0,
            "tipo_producto": "Agricola"
        }
        res = requests.post(f"{BASE_URL}/eventos", json=payload)
        self.assertEqual(res.status_code, 200, "No se pudo registrar el evento de calidad")
        print("[OK] CU3: Evento de calidad (Mínimos y Máximos) registrado")

    def test_04_cu7_validar_vacio(self):
        """Prueba del Caso de Uso 7: Validación cuando el lote no tiene evaluaciones (Bloqueo esperado)"""
        # Intentamos obtener reporte estadístico (CU5/CU6) de un lote que aún no ha sido evaluado en CU4
        res = requests.get(f"{BASE_URL}/reportes/estadisticas/{self.lote_id}")
        self.assertEqual(res.status_code, 400, "El sistema debió bloquear (400) la consulta por falta de datos.")
        self.assertIn("no tiene evaluaciones", res.json()["detail"])
        print("[OK] CU7: Validación correcta (El sistema bloqueó y avisó la ausencia de datos)")

    def test_05_cu4_evaluacion_automatica(self):
        """Prueba del Caso de Uso 4: Registro de Evaluación Automática"""
        payload = {
            "lote_id": self.lote_id,
            "cod_inspeccion": f"INS-LAB-{self.random_suffix}",
            "fecha_control": "2026-07-16"
        }
        res = requests.post(f"{BASE_URL}/evaluacion", json=payload)
        self.assertEqual(res.status_code, 200, "Fallo al generar evaluación automática")
        metricas = res.json()
        self.assertTrue(len(metricas) > 0, "No se generaron métricas de laboratorio")
        self.assertIn(metricas[0]["estado"], ["APROBADO", "DESAPROBADO"])
        print(f"[OK] CU4: Laboratorio virtual generó {len(metricas)} resultados exitosamente")

    def test_06_cu5_graficos_estadisticos(self):
        """Prueba del Caso de Uso 5: Generar reporte de gráficos estadísticos"""
        res = requests.get(f"{BASE_URL}/reportes/estadisticas/{self.lote_id}")
        self.assertEqual(res.status_code, 200, "No se pudieron obtener las estadísticas para gráficos")
        data = res.json()
        self.assertTrue("aprobados" in data and "desaprobados" in data, "Faltan los datos consolidados")
        print(f"[OK] CU5: Datos estadísticos extraídos para gráficos ({data['aprobados']} Óptimos, {data['desaprobados']} Defectos)")

    def test_07_cu6_generar_informe(self):
        """Prueba del Caso de Uso 6: Consolidación de informe de estado de calidad (PDF)"""
        res = requests.get(f"{BASE_URL}/reportes/estadisticas/{self.lote_id}")
        self.assertEqual(res.status_code, 200, "No se pudieron obtener los datos para el informe PDF")
        data = res.json()
        self.assertEqual(data["lote_codigo"], self.lote_codigo, "El código del lote no coincide en el informe")
        self.assertIsNotNone(data["fecha_control"], "Falta la fecha de control para el reporte final")
        print(f"[OK] CU6: Informe técnico consolidado exitosamente para el Lote {self.lote_codigo}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
