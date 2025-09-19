from fastapi import FastAPI, Depends
import os
from datetime import datetime
from apis.endpoints import clientes as clientes_router
from apis.endpoints import cuentas as cuentas_router
from apis.endpoints import transacciones as transacciones_router
from apis.database.connection import engine, Base, get_db, get_database_status
from sqlalchemy.orm import Session
from apis.scripts.migrate_json_to_db import migrate_json_to_db

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Bancaria G1 - Versión con SQL Server",
    description="API para sistema bancario con funcionalidades básicas y persistencia en SQL Server",
    version="1.0.0"
)

from apis.models.schemas import ClienteSimple, CuentaSimple, TransaccionSimple
from apis.models.models import Cliente, Cuenta, Transaccion

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    try:
        print("Iniciando API Bancaria con SQL Server...")
        # Crear las tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas o verificadas correctamente")
        
        # Verificar la conexión a la base de datos
        print("Verificando conexión a la base de datos...")
        db_status = get_database_status()
        print(f"Estado de la base de datos: {db_status['status']}")
        print(f"Tipo de base de datos: {db_status['type']}")
        
        # Migrar datos JSON a la base de datos
        print("Migrando datos JSON a la base de datos...")
        migrate_json_to_db()
        print("API iniciada correctamente")
    except Exception as e:
        print(f"Error al inicializar la API: {e}")

# Ruta raíz
@app.get("/", tags=["Información"],
         summary="Información general de la API",
         description="Endpoint principal que proporciona información general sobre la API bancaria, incluyendo versión y endpoints disponibles.",
         response_description="Información general de la API bancaria")
def read_root():
    """Información general de la API bancaria"""
    return {
        "message": "API Bancaria G1 - Versión con SQL Server",
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
         response_description="Información detallada del estado de salud de la API")
def health_check(db: Session = Depends(get_db)):
    """Verificación de estado de la API"""
    # Verificar conexión a la base de datos
    db_status = get_database_status()
    
    # Contar registros (usando SQLAlchemy)
    try:
        num_clientes = db.query(Cliente).count()
        num_cuentas = db.query(Cuenta).count()
        num_transacciones = db.query(Transaccion).count()
        db_connected = True
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        num_clientes = 0
        num_cuentas = 0
        num_transacciones = 0
        db_connected = False
    
    # Calcular tiempo de actividad (simulado)
    uptime = "1h 30m 45s"  # En una aplicación real, se calcularía desde el inicio
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "message": "API funcionando correctamente" if db_connected else "Problemas de conexión con la base de datos",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": uptime,
        "database": {
            "status": db_status["status"],
            "type": db_status["type"],
            "records": {
                "clientes": num_clientes,
                "cuentas": num_cuentas,
                "transacciones": num_transacciones
            }
        }
    }

# Routers de negocio
app.include_router(clientes_router.router)
app.include_router(cuentas_router.router)
app.include_router(transacciones_router.router)

if __name__ == "__main__":
    import uvicorn
    print("Iniciando API Bancaria G1 - Versión con SQL Server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
