from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional

from apis.models.schemas import (
    TransaccionSimple,
    OperacionConsignacion,
    OperacionRetiro,
    OperacionTransferencia,
)


router = APIRouter(prefix="/transacciones", tags=["Transacciones"])


@router.get("", summary="Obtener lista de transacciones", response_model=List[TransaccionSimple])
def obtener_transacciones(request: Request, tipo_transaccion: Optional[str] = Query(None, description="Filtrar por tipo de transacción (Consignación, Retiro, Transferencia, etc.)")):
    """Obtener lista de transacciones"""
    transacciones_db = request.app.state.transacciones_db
    if tipo_transaccion:
        filtradas = [t for t in transacciones_db if t["tipoTransaccion"].lower() == tipo_transaccion.lower()]
        if not filtradas:
            raise HTTPException(status_code=404, detail=f"No se encontraron transacciones con tipo: {tipo_transaccion}")
        return filtradas
    return transacciones_db


@router.get("/{id_transaccion}", summary="Obtener transacción por ID", response_model=TransaccionSimple)
def obtener_transaccion(request: Request, id_transaccion: int):
    """Obtener transacción por ID"""
    transacciones_db = request.app.state.transacciones_db
    for transaccion in transacciones_db:
        if transaccion["idTransaccion"] == id_transaccion:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router.post("", summary="Crear nueva transacción", status_code=201, response_model=TransaccionSimple)
def crear_transaccion(request: Request, transaccion: TransaccionSimple):
    """Crear nueva transacción"""
    transacciones_db = request.app.state.transacciones_db
    for t in transacciones_db:
        if t["idTransaccion"] == transaccion.idTransaccion:
            raise HTTPException(status_code=400, detail="El ID de la transacción ya existe")
    transaccion_dict = transaccion.model_dump()
    transacciones_db.append(transaccion_dict)
    return transaccion_dict


@router.put("/{id_transaccion}", summary="Actualizar transacción", response_model=TransaccionSimple)
def actualizar_transaccion(request: Request, id_transaccion: int, transaccion: TransaccionSimple):
    """Actualizar transacción"""
    transacciones_db = request.app.state.transacciones_db
    for i, t in enumerate(transacciones_db):
        if t["idTransaccion"] == id_transaccion:
            transaccion_dict = transaccion.model_dump()
            transacciones_db[i] = transaccion_dict
            return transaccion_dict
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router.delete("/{id_transaccion}", summary="Eliminar transacción")
def eliminar_transaccion(request: Request, id_transaccion: int):
    """Eliminar transacción"""
    transacciones_db = request.app.state.transacciones_db
    for i, t in enumerate(transacciones_db):
        if t["idTransaccion"] == id_transaccion:
            transacciones_db.pop(i)
            return {"mensaje": f"Transacción {id_transaccion} eliminada"}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router.post("/consignar", summary="Realizar consignación")
def consignar(request: Request, operacion: OperacionConsignacion):
    """Realizar consignación"""
    cuentas_db = request.app.state.cuentas_db
    cuenta_encontrada = next((c for c in cuentas_db if c["numeroCuenta"] == operacion.numeroCuenta), None)
    if not cuenta_encontrada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    saldo_anterior = cuenta_encontrada["saldoActual"]
    saldo_nuevo = saldo_anterior + operacion.monto
    return {
        "mensaje": "Consignación exitosa",
        "operacion": operacion.model_dump(),
        "tipo": "consignacion",
        "saldoAnterior": saldo_anterior,
        "saldoNuevo": saldo_nuevo,
    }


@router.post("/retirar", summary="Realizar retiro")
def retirar(request: Request, operacion: OperacionRetiro):
    """Realizar retiro"""
    cuentas_db = request.app.state.cuentas_db
    cuenta_encontrada = next((c for c in cuentas_db if c["numeroCuenta"] == operacion.numeroCuenta), None)
    if not cuenta_encontrada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    saldo_anterior = cuenta_encontrada["saldoActual"]
    if saldo_anterior < operacion.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar el retiro")
    saldo_nuevo = saldo_anterior - operacion.monto
    return {
        "mensaje": "Retiro exitoso",
        "operacion": operacion.model_dump(),
        "tipo": "retiro",
        "saldoAnterior": saldo_anterior,
        "saldoNuevo": saldo_nuevo,
    }


@router.post("/transferir", summary="Realizar transferencia")
def transferir(request: Request, transferencia: OperacionTransferencia):
    """Realizar transferencia"""
    if transferencia.numeroCuentaOrigen == transferencia.numeroCuentaDestino:
        raise HTTPException(status_code=400, detail="No se puede transferir a la misma cuenta")
    cuentas_db = request.app.state.cuentas_db
    cuenta_origen = next((c for c in cuentas_db if c["numeroCuenta"] == transferencia.numeroCuentaOrigen), None)
    cuenta_destino = next((c for c in cuentas_db if c["numeroCuenta"] == transferencia.numeroCuentaDestino), None)
    if not cuenta_origen or not cuenta_destino:
        raise HTTPException(status_code=404, detail="Cuenta origen o destino no encontrada")
    saldo_origen_anterior = cuenta_origen["saldoActual"]
    saldo_destino_anterior = cuenta_destino["saldoActual"]
    if saldo_origen_anterior < transferencia.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar la transferencia")
    saldo_origen_nuevo = saldo_origen_anterior - transferencia.monto
    saldo_destino_nuevo = saldo_destino_anterior + transferencia.monto
    return {
        "mensaje": "Transferencia exitosa",
        "transferencia": transferencia.model_dump(),
        "tipo": "transferencia",
        "saldoOrigenAnterior": saldo_origen_anterior,
        "saldoOrigenNuevo": saldo_origen_nuevo,
        "saldoDestinoAnterior": saldo_destino_anterior,
        "saldoDestinoNuevo": saldo_destino_nuevo,
    }


