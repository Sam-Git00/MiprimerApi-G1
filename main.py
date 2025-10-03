"""
Sistema de Gestión Médica - API Principal

Este módulo contiene la configuración principal de la API FastAPI
para el sistema de gestión médica, incluyendo la configuración de CORS,
registro de routers y la función principal de ejecución.
"""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.migrations import print_migration_status, run_migrations
from src.routers import (
    cheques,
    clientes,
    cuentas,
    empleados,
    prestamos,
    auth,
    tarjetas,
    transacciones,
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para manejar pacientes, médicos y citas médicas.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Cheques",
            "description": "Operaciones relacionadas con el manejo de cheques.",
        },
        {"name": "Clientes", "description": "Gestión de información de clientes."},
        {"name": "Cuentas", "description": "Gestión de información de cuentas."},
        {"name": "Empleados", "description": "Gestión de información de empleados."},
        {"name": "Préstamos", "description": "Gestión de información de préstamos."},
        {"name": "Tarjetas", "description": "Gestión de información de tarjetas."},
        {"name": "Transacciones", "description": "Gestión de información de transacciones."},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router de autenticación (sin protección)
app.include_router(auth.router)

# Incluir routers médicos (con protección JWT)
app.include_router(cheques.router)
app.include_router(clientes.router)
app.include_router(cuentas.router)
app.include_router(empleados.router)
app.include_router(prestamos.router)
app.include_router(tarjetas.router)
app.include_router(transacciones.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://mi-frontend.com",
]


@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio que ejecuta la migración automática de la base de datos.
    """
    logger.info("Iniciando Sistema de Gestión Médica...")

    try:
        logger.info("Ejecutando migración automática...")
        migration_success = run_migrations()

        if migration_success:
            logger.info("Migración completada exitosamente")
            print_migration_status()
        else:
            logger.error(
                "Error en la migración - la aplicación puede no funcionar correctamente"
            )

    except Exception as e:
        logger.error(f"Error crítico durante el inicio: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento de cierre de la aplicación.
    """
    logger.info("🛑 Cerrando Sistema de Gestión Médica...")


def main():
    """
    Función principal para ejecutar el servidor FastAPI.

    Configura y ejecuta el servidor con uvicorn, habilitando el modo de recarga
    automática para desarrollo y configurando el host y puerto apropiados.
    """
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
