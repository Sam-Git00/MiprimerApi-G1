
from fastapi import FastAPI
import json
import os
from datetime import datetime
from apis.endpoints import clientes as clientes_router
from apis.endpoints import cuentas as cuentas_router
from apis.endpoints import transacciones as transacciones_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Bancaria G1 - Versión Simplificada",
    description="API para sistema bancario con funcionalidades básicas",
    version="1.0.0"
)

from apis.models.schemas import ClienteSimple, CuentaSimple, TransaccionSimple

# Datos en memoria (simulando base de datos)
clientes_db = []
cuentas_db = []
transacciones_db = []

def cargar_datos():
    """Carga de datos desde JSON"""
    try:
        # Cargar clientes
        if os.path.exists("datos/clientes.json"):
            with open("datos/clientes.json", 'r', encoding='utf-8') as f:
                clientes_db.extend(json.load(f))
        
        # Cargar cuentas
        if os.path.exists("datos/cuentas.json"):
            with open("datos/cuentas.json", 'r', encoding='utf-8') as f:
                cuentas_db.extend(json.load(f))
        
        # Cargar transacciones
        if os.path.exists("datos/transacciones.json"):
            with open("datos/transacciones.json", 'r', encoding='utf-8') as f:
                transacciones_db.extend(json.load(f))
                
        print(f"✅ Datos cargados: {len(clientes_db)} clientes, {len(cuentas_db)} cuentas, {len(transacciones_db)} transacciones")
    except Exception as e:
        print(f" Error cargando datos: {e}")

# Cargar datos al iniciar y exponerlos en app.state
app.state.clientes_db = clientes_db
app.state.cuentas_db = cuentas_db
app.state.transacciones_db = transacciones_db
cargar_datos()

# Ruta raíz
@app.get("/", tags=["Información"],
         summary="Información general de la API",
         description="Endpoint principal que proporciona información general sobre la API bancaria, incluyendo versión y endpoints disponibles.",
         response_description="Información general de la API bancaria")
def read_root():
    """Información general de la API bancaria"""
    return {
        "message": "API Bancaria G1 - Versión Simplificada",
        "version": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "cuentas": "/cuentas", 
            "transacciones": "/transacciones"
        },
        "documentación": "/docs"
    }

@app.get("/health", tags=["Salud"], 
         summary="Verificar estado de la API",
         description="Endpoint para verificar que la API esté funcionando correctamente. Retorna información detallada sobre el estado del servicio, incluyendo métricas y timestamp.",
         response_description="Información detallada del estado de salud de la API",
         responses={
             200: {
                 "description": "API funcionando correctamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "healthy",
                             "message": "API funcionando correctamente",
                             "timestamp": "2024-01-15T10:30:00",
                             "version": "1.0.0",
                             "uptime": "2h 15m 30s",
                             "databases": {
                                 "clientes": 4,
                                 "cuentas": 3,
                                 "transacciones": 2
                             }
                         }
                     }
                 }
             }
         })
def health_check():
    """Verificación de estado de la API"""
    # Verificar archivos de datos
    archivos_ok = all([
        os.path.exists("datos/clientes.json"),
        os.path.exists("datos/cuentas.json"),
        os.path.exists("datos/transacciones.json")
    ])
    
    # Determinar estado basado en verificaciones
    if archivos_ok and len(clientes_db) > 0:
        status = "healthy"
        message = "API funcionando correctamente"
    elif archivos_ok:
        status = "degraded"
        message = "API funcionando pero sin datos cargados"
    else:
        status = "unhealthy"
        message = "Problemas con archivos de datos"
    
    # Simular uptime (en un caso real se calcularía desde el inicio)
    uptime = "2h 15m 30s"  # Simulado
    
    return {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": uptime,
        "databases": {
            "clientes": len(clientes_db),
            "cuentas": len(cuentas_db),
            "transacciones": len(transacciones_db)
        }
    }

# Routers de negocio
app.include_router(clientes_router.router)
app.include_router(cuentas_router.router)
app.include_router(transacciones_router.router)
    


if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API Bancaria G1 - Versión Simplificada...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
