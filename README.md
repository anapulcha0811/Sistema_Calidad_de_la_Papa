# Sistema de Información AgroTalavera

Este repositorio contiene el sistema de control de calidad para AgroTalavera, dividido en un backend (API REST con FastAPI) y un frontend (Aplicación Web con Flask), ambos soportados por una base de datos PostgreSQL.

## 1. Requisitos Previos

Asegúrese de ejecutar los comandos en un sistema basado en Ubuntu/Debian. Se requieren privilegios de administrador.

Actualice su sistema e instale PostgreSQL y las herramientas de Python necesarias:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib python3 python3-pip python3-venv git curl -y
```

## 2. Configuración de la Base de Datos (PostgreSQL)

El sistema utiliza PostgreSQL. Debe crear un usuario y una base de datos específica para el proyecto.

Ejecute los siguientes comandos en la terminal:

```bash
sudo -u postgres psql -c "CREATE USER agro_user WITH PASSWORD 'agro_pass';"
sudo -u postgres psql -c "CREATE DATABASE agrotalavera OWNER agro_user;"
```

## 3. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd prueba
```
*(Nota: Reemplace `<URL_DEL_REPOSITORIO>` por la URL de su repositorio en GitHub).*

## 4. Instalación y Ejecución del Backend

El backend gestiona la lógica de negocio y la conexión con la base de datos.

```bash
cd agro-talavera-backend

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar la base de datos y cargar datos maestros
python seed_db.py

# Ejecutar el servidor backend
python main.py
```
El backend estará corriendo en `http://localhost:8000`.

## 5. Instalación y Ejecución del Frontend

Abra una **nueva pestaña o ventana de terminal** y navegue a la carpeta del frontend.

```bash
cd /ruta/a/prueba/agro-talavera-flask-frontend

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor frontend web
python3 app.py
```
El frontend estará corriendo en `http://0.0.0.0:5000`.

## 6. Configuración de Acceso Externo (Red Local)

Por defecto, el frontend y backend funcionan correctamente si se abren los navegadores dentro de la misma máquina (Ubuntu). 

Si desea acceder al sistema web desde otra computadora en la misma red (por ejemplo, desde la máquina host):

1. Averigüe la IP de la máquina Ubuntu ejecutando el comando `ip a`.
2. En el archivo `agro-talavera-flask-frontend/templates/`, el código JavaScript está configurado para leer dinámicamente la IP mediante `window.location.hostname`.
3. Abra el navegador en su máquina externa y acceda a `http://<IP_DE_UBUNTU>:5000`.

Para permitir conexiones de clientes SQL externos (como pgAdmin o DBeaver) a PostgreSQL, debe editar los archivos `postgresql.conf` y `pg_hba.conf` en `/etc/postgresql/18/main/` (o la versión instalada) para permitir `listen_addresses = '*'` y configurar los rangos de IPs permitidos.
# Sistema_Calidad_de_la_Papa
# Sistema_Calidad_de_la_Papa
# Sistema_Calidad_de_la_Papa
# Sistema_Calidad_de_la_Papa
