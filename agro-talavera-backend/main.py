from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine, Base
from controllers import auth_controller, cultivo_controller, calidad_controller, reporte_controller

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Backend - AgroTalavera")

# Configurar CORS (Permite que el frontend en Windows llame a esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar por la IP específica del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los routers de las diferentes capas lógicas
app.include_router(auth_controller.router)
app.include_router(cultivo_controller.router)
app.include_router(calidad_controller.router)
app.include_router(reporte_controller.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Backend de AgroTalavera. Dirígete a /docs para ver los endpoints."}
