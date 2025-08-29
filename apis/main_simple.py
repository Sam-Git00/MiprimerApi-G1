from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import json
import os

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Bancaria G1 - Versión Simplificada",
    description="API para sistema bancario con funcionalidades básicas",
    version="1.0.0"
)

# Modelos Pydantic simplificados
class ClienteSimple(BaseModel):
    idCliente: int
    nombreCompleto: str
    correoElectronico: str
    numeroTelefono: str
    numeroDocumento: str
    tipoDocumento: str

class CuentaSimple(BaseModel):
    numeroCuenta: str
    idCliente: int
    tipoCuenta: str
    saldoActual: float
    estadoCuenta: str

class TransaccionSimple(BaseModel):
    idTransaccion: int
    numeroCuentaOrigen: str
    tipoTransaccion: str
    montoTransaccion: float
    descripcionTransaccion: str

# Datos en memoria (simulando base de datos)
clientes_db = []
cuentas_db = []
transacciones_db = []

def cargar_datos():
    """Carga datos desde archivos JSON"""
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
        print(f"⚠️ Error cargando datos: {e}")

# Cargar datos al iniciar
cargar_datos()

# Ruta raíz
@app.get("/", tags=["Información"])
def read_root():
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

@app.get("/health", tags=["Salud"])
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

# ===== ENDPOINTS DE CLIENTES =====
@app.get("/clientes", tags=["Clientes"], response_model=List[ClienteSimple])
def obtener_clientes(tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento")):
    """Obtener todos los clientes con filtros opcionales"""
    if tipo_documento:
        return [c for c in clientes_db if c["tipoDocumento"].lower() == tipo_documento.lower()]
    return clientes_db

@app.get("/clientes/{id_cliente}", tags=["Clientes"], response_model=ClienteSimple)
def obtener_cliente(id_cliente: int):
    """Obtener cliente por ID"""
    for cliente in clientes_db:
        if cliente["idCliente"] == id_cliente:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.post("/clientes", tags=["Clientes"], status_code=201, response_model=ClienteSimple)
def crear_cliente(cliente: ClienteSimple):
    """Crear nuevo cliente"""
    # Validar que no exista el ID
    for c in clientes_db:
        if c["idCliente"] == cliente.idCliente:
            raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
    
    cliente_dict = cliente.model_dump()
    clientes_db.append(cliente_dict)
    return cliente_dict

@app.put("/clientes/{id_cliente}", tags=["Clientes"], response_model=ClienteSimple)
def actualizar_cliente(id_cliente: int, cliente: ClienteSimple):
    """Actualizar cliente"""
    for i, c in enumerate(clientes_db):
        if c["idCliente"] == id_cliente:
            cliente_dict = cliente.model_dump()
            clientes_db[i] = cliente_dict
            return cliente_dict
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.delete("/clientes/{id_cliente}", tags=["Clientes"])
def eliminar_cliente(id_cliente: int):
    """Eliminar cliente"""
    for i, c in enumerate(clientes_db):
        if c["idCliente"] == id_cliente:
            clientes_db.pop(i)
            return {"mensaje": f"Cliente {id_cliente} eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# ===== ENDPOINTS DE CUENTAS =====
@app.get("/cuentas", tags=["Cuentas"], response_model=List[CuentaSimple])
def obtener_cuentas(tipo_cuenta: Optional[str] = Query(None, description="Filtrar por tipo de cuenta")):
    """Obtener todas las cuentas con filtros opcionales"""
    if tipo_cuenta:
        return [c for c in cuentas_db if c["tipoCuenta"].lower() == tipo_cuenta.lower()]
    return cuentas_db

@app.get("/cuentas/{numero_cuenta}", tags=["Cuentas"], response_model=CuentaSimple)
def obtener_cuenta(numero_cuenta: str):
    """Obtener cuenta por número"""
    for cuenta in cuentas_db:
        if cuenta["numeroCuenta"] == numero_cuenta:
            return cuenta
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")

@app.post("/cuentas", tags=["Cuentas"], status_code=201, response_model=CuentaSimple)
def crear_cuenta(cuenta: CuentaSimple):
    """Crear nueva cuenta"""
    cuenta_dict = cuenta.model_dump()
    cuentas_db.append(cuenta_dict)
    return cuenta_dict

# ===== ENDPOINTS DE TRANSACCIONES =====
@app.get("/transacciones", tags=["Transacciones"], response_model=List[TransaccionSimple])
def obtener_transacciones(tipo_transaccion: Optional[str] = Query(None, description="Filtrar por tipo de transacción")):
    """Obtener todas las transacciones con filtros opcionales"""
    if tipo_transaccion:
        return [t for t in transacciones_db if t["tipoTransaccion"].lower() == tipo_transaccion.lower()]
    return transacciones_db

@app.get("/transacciones/{id_transaccion}", tags=["Transacciones"], response_model=TransaccionSimple)
def obtener_transaccion(id_transaccion: int):
    """Obtener transacción por ID"""
    for transaccion in transacciones_db:
        if transaccion["idTransaccion"] == id_transaccion:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

# ===== ENDPOINTS ESPECIALES =====
@app.post("/transacciones/consignar", tags=["Transacciones"], status_code=201)
def consignar(operacion: dict):
    """Realizar consignación a una cuenta"""
    return {
        "mensaje": "Consignación exitosa",
        "operacion": operacion,
        "tipo": "consignacion"
    }

@app.post("/transacciones/retirar", tags=["Transacciones"], status_code=201)
def retirar(operacion: dict):
    """Realizar retiro de una cuenta"""
    return {
        "mensaje": "Retiro exitoso",
        "operacion": operacion,
        "tipo": "retiro"
    }

@app.post("/transacciones/transferir", tags=["Transacciones"], status_code=201)
def transferir(transferencia: dict):
    """Realizar transferencia entre cuentas"""
    return {
        "mensaje": "Transferencia exitosa",
        "transferencia": transferencia,
        "tipo": "transferencia"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API Bancaria G1 - Versión Simplificada...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
