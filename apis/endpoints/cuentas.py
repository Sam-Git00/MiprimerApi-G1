from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional

from apis.models.schemas import CuentaSimple


router = APIRouter(prefix="/cuentas", tags=["Cuentas"])


@router.get("", summary="Obtener lista de cuentas", response_model=List[CuentaSimple])
def obtener_cuentas(request: Request, tipo_cuenta: Optional[str] = Query(None, description="Filtrar por tipo de cuenta (Ahorros, Corriente, etc.)")):
    """Obtener lista de cuentas"""
    cuentas_db = request.app.state.cuentas_db
    if tipo_cuenta:
        cuentas_filtradas = [c for c in cuentas_db if c["tipoCuenta"].lower() == tipo_cuenta.lower()]
        if not cuentas_filtradas:
            raise HTTPException(status_code=404, detail=f"No se encontraron cuentas con tipo: {tipo_cuenta}")
        return cuentas_filtradas
    return cuentas_db


@router.get("/{numero_cuenta}", summary="Obtener cuenta por número", response_model=CuentaSimple)
def obtener_cuenta(request: Request, numero_cuenta: str):
    """Obtener cuenta por número"""
    cuentas_db = request.app.state.cuentas_db
    for cuenta in cuentas_db:
        if cuenta["numeroCuenta"] == numero_cuenta:
            return cuenta
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")


@router.post("", summary="Crear nueva cuenta", status_code=201, response_model=CuentaSimple)
def crear_cuenta(request: Request, cuenta: CuentaSimple):
    """Crear nueva cuenta"""
    cuentas_db = request.app.state.cuentas_db
    cuenta_dict = cuenta.model_dump()
    cuentas_db.append(cuenta_dict)
    return cuenta_dict


@router.put("/{numero_cuenta}", summary="Actualizar cuenta", response_model=CuentaSimple)
def actualizar_cuenta(request: Request, numero_cuenta: str, cuenta: CuentaSimple):
    """Actualizar cuenta"""
    cuentas_db = request.app.state.cuentas_db
    for i, c in enumerate(cuentas_db):
        if c["numeroCuenta"] == numero_cuenta:
            cuenta_dict = cuenta.model_dump()
            cuentas_db[i] = cuenta_dict
            return cuenta_dict
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")


@router.delete("/{numero_cuenta}", summary="Eliminar cuenta")
def eliminar_cuenta(request: Request, numero_cuenta: str):
    """Eliminar cuenta"""
    cuentas_db = request.app.state.cuentas_db
    for i, c in enumerate(cuentas_db):
        if c["numeroCuenta"] == numero_cuenta:
            cuentas_db.pop(i)
            return {"mensaje": f"Cuenta {numero_cuenta} eliminada"}
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")


