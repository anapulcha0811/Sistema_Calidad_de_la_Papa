import requests

BASE_URL = "http://127.0.0.1:8000/api"

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        
    def login(self, username, password):
        """Intenta iniciar sesión en el backend."""
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                json={"usuario": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                return True, "Login exitoso"
            else:
                return False, "Credenciales inválidas"
        except requests.exceptions.RequestException:
            return False, "Error al conectar con el servidor"

    def get_lotes(self):
        try:
            response = self.session.get(f"{BASE_URL}/lotes", timeout=5)
            if response.status_code == 200:
                return True, response.json()
            return False, "Error al cargar lotes"
        except requests.exceptions.RequestException:
            return False, "Error de conexión"
            
    def create_lote(self, data):
        try:
            response = self.session.post(f"{BASE_URL}/lotes", json=data, timeout=5)
            if response.status_code == 200:
                return True, "Lote registrado con éxito"
            return False, "Error al registrar lote"
        except requests.exceptions.RequestException:
            return False, "Error de conexión"

    def delete_lote(self, lote_id):
        try:
            response = self.session.delete(f"{BASE_URL}/lotes/{lote_id}", timeout=5)
            if response.status_code == 200:
                return True, "Lote eliminado exitosamente"
            return False, "Error al eliminar lote"
        except requests.exceptions.RequestException:
            return False, "Error de conexión"

    def update_lote(self, lote_id, data):
        try:
            # Asumiendo que existe un endpoint PUT o PATCH en fastapi
            response = self.session.put(f"{BASE_URL}/lotes/{lote_id}", json=data, timeout=5)
            if response.status_code == 200:
                return True, "Lote actualizado exitosamente"
            return False, "Error al actualizar lote"
        except requests.exceptions.RequestException:
            return False, "Error de conexión"
