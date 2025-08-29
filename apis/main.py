from fastapi import FastAPI
from vistas.cliente_vista import router as cliente_router
from vistas.cuenta_vista import router as cuenta_router
from vistas.transaccion_vista import router as transaccion_router
from vistas.auth_vista import router as auth_router

app = FastAPI(
    title="API Bancaria G1",
    description="API completa para un sistema bancario con arquitectura de 3 capas",
    version="1.0.0"
)

# Incluir todos los routers
app.include_router(cliente_router)
app.include_router(cuenta_router)
app.include_router(transaccion_router)
app.include_router(auth_router)

# Ruta raíz
@app.get("/", tags=["Información"])
def read_root():
    return {
        "message": "API Bancaria G1 - Sistema de Gestión Bancaria",
        "version": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "cuentas": "/cuentas", 
            "transacciones": "/transacciones",
            "autenticación": "/auth"
        },
        "documentación": "/docs"
    }

@app.get("/health", tags=["Salud"])
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

# Los endpoints ahora vienen de los routers de las vistas
    